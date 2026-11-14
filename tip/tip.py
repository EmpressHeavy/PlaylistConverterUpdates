#!/usr/bin/env python3
"""Local conversion counter and tip-prompt cadence for Playlist Converter.

Stores a few rows in the same SQLite file as mem (MEM_DB, default
/workspace/memory/brain.db), table tip_state. Stdlib only. No network.

record / later / monthly / status / setup-start / setup-complete always
exit 0. A database problem prints show=no and reason=error so a conversion
is never blocked. There is no command that turns the prompt off for good.
"""
import datetime, os, sqlite3, sys

DB = os.environ.get('MEM_DB', '/workspace/memory/brain.db')
FIRST_COUNT = 3
WEEK = 7
MONTH = 30
USAGE = ('tip record [--date YYYY-MM-DD] | later [--date YYYY-MM-DD] | '
         'monthly [--date YYYY-MM-DD] | status [--date YYYY-MM-DD] | '
         'setup-start | setup-complete')

def connect(path):
    c = sqlite3.connect(path, isolation_level=None)
    c.execute('PRAGMA busy_timeout=30000')
    c.execute('PRAGMA journal_mode=WAL')
    c.execute('CREATE TABLE IF NOT EXISTS tip_state(k TEXT PRIMARY KEY, v TEXT)')
    return c

def _get(c, k):
    r = c.execute('SELECT v FROM tip_state WHERE k=?', (k,)).fetchone()
    return r[0] if r else None

def _put(c, k, v):
    c.execute('INSERT OR REPLACE INTO tip_state(k,v) VALUES(?,?)', (k, v))

def cadence_of(value):
    """Only 30 is the slower cadence. Anything else stays a week.
    A stored "never", 0, or huge number is not an opt-out."""
    try:
        if int(str(value).strip()) == MONTH:
            return MONTH
    except (TypeError, ValueError):
        pass
    return WEEK

def setup_of(value):
    """Only an explicit in-progress flag hides the prompt. Anything else,
    including a missing row, means setup is finished (upgrades included)."""
    return 'in_progress' if value == 'in_progress' else 'complete'

def parse_shown(value):
    if not value:
        return None
    try:
        return datetime.date.fromisoformat(str(value).strip())
    except ValueError:
        return None

def should_show(conversions, last_shown, cadence_days, setup, today):
    """Whether to show the tip prompt after this completed conversion.

    conversions is the count including the conversion that just finished.
    last_shown is a date, an ISO date string, or None.
    Returns (show, reason). Reasons: setup, count, cadence, due.
    A future last_shown is ignored so a bad date cannot hide the prompt for good.
    """
    if setup_of(setup) == 'in_progress':
        return False, 'setup'
    try:
        n = int(conversions)
    except (TypeError, ValueError):
        n = 0
    if n < FIRST_COUNT:
        return False, 'count'
    shown = last_shown if isinstance(last_shown, datetime.date) else parse_shown(last_shown)
    if shown is not None and shown > today:
        shown = None
    if shown is not None and (today - shown).days < cadence_of(cadence_days):
        return False, 'cadence'
    return True, 'due'

def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def _read(c):
    return {
        'conversions': _int(_get(c, 'conversions') or 0),
        'cadence_days': cadence_of(_get(c, 'cadence_days')),
        'setup': setup_of(_get(c, 'setup')),
        'last_shown': parse_shown(_get(c, 'last_shown')),
        'show': False,
        'reason': 'status',
    }

def _blank():
    return {'conversions': '', 'cadence_days': '', 'setup': '', 'last_shown': '',
            'show': False, 'reason': 'error'}

def format_result(st):
    shown = st['last_shown']
    if isinstance(shown, datetime.date):
        shown = shown.isoformat()
    cadence = st['cadence_days']
    return '\n'.join([
        'conversions=%s' % st['conversions'],
        'cadence_days=%s' % cadence,
        'setup=%s' % st['setup'],
        'last_shown=%s' % (shown or ''),
        'show=%s' % ('yes' if st['show'] else 'no'),
        'reason=%s' % st['reason'],
    ])

def record(c, today):
    c.execute('BEGIN IMMEDIATE')
    try:
        st = _read(c)
        st['conversions'] += 1
        show, reason = should_show(st['conversions'], st['last_shown'], st['cadence_days'], st['setup'], today)
        st['show'], st['reason'] = show, reason
        _put(c, 'conversions', str(st['conversions']))
        if show:
            st['last_shown'] = today
            _put(c, 'last_shown', today.isoformat())
        c.execute('COMMIT')
        return st
    except Exception:
        try: c.execute('ROLLBACK')
        except sqlite3.Error: pass
        raise

def _choose(c, today, cadence, reason):
    c.execute('BEGIN IMMEDIATE')
    try:
        st = _read(c)
        st['cadence_days'] = cadence
        st['last_shown'] = today
        st['show'] = False
        st['reason'] = reason
        _put(c, 'cadence_days', str(cadence))
        _put(c, 'last_shown', today.isoformat())
        c.execute('COMMIT')
        return st
    except Exception:
        try: c.execute('ROLLBACK')
        except sqlite3.Error: pass
        raise

def later(c, today):
    """Maybe later. Keeps the 7-day cadence so the prompt can show again next week."""
    return _choose(c, today, WEEK, 'later')

def monthly(c, today):
    """Remind me monthly, or the prompt was dismissed without a choice. At most once every 30 days."""
    return _choose(c, today, MONTH, 'monthly')

def status(c, today):
    st = _read(c)
    st['show'] = False
    st['reason'] = 'status'
    return st

def setup_start(c, today):
    _put(c, 'setup', 'in_progress')
    st = _read(c)
    st['show'] = False
    st['reason'] = 'setup'
    return st

def setup_complete(c, today):
    _put(c, 'setup', 'complete')
    st = _read(c)
    st['show'] = False
    st['reason'] = 'setup_complete'
    return st

COMMANDS = {
    'record': record,
    'later': later,
    'monthly': monthly,
    'status': status,
    'setup-start': setup_start,
    'setup-complete': setup_complete,
}

def parse_args(argv):
    if not argv or argv[0] in ('-h', '--help') or argv[0] not in COMMANDS:
        raise ValueError('usage')
    cmd, rest, today = argv[0], argv[1:], None
    if '--date' in rest:
        i = rest.index('--date')
        if i + 1 >= len(rest):
            raise ValueError('date')
        today = datetime.date.fromisoformat(rest[i + 1])
        rest = rest[:i] + rest[i + 2:]
    if rest:
        raise ValueError('extra')
    return cmd, today or datetime.date.today()

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    try:
        cmd, today = parse_args(argv)
    except ValueError:
        print(USAGE, file=sys.stderr)
        return 2
    path = os.environ.get('MEM_DB', DB)
    try:
        c = connect(path)
        print(format_result(COMMANDS[cmd](c, today)))
        return 0
    except Exception:
        print(format_result(_blank()))
        return 0

if __name__ == '__main__':
    sys.exit(main())
