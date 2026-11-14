#!/usr/bin/env python3
"""Counter and cadence tests for the tip prompt. Stdlib unittest only."""
import datetime, os, sqlite3, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import generate_qr
import tip

PROMPT = generate_qr.PROMPT
LINKS = generate_qr.LINKS

def parse(text):
    out = {}
    for line in text.strip().splitlines():
        k, _, v = line.partition('=')
        out[k] = v
    return out

class DecideTests(unittest.TestCase):
    day0 = datetime.date(2026, 11, 1)

    def test_hides_before_three_completed_conversions(self):
        for n in (0, 1, 2):
            show, reason = tip.should_show(n, None, 7, 'complete', self.day0)
            self.assertEqual((show, reason), (False, 'count'))

    def test_shows_on_the_third(self):
        show, reason = tip.should_show(3, None, 7, 'complete', self.day0)
        self.assertEqual((show, reason), (True, 'due'))

    def test_week_boundary_is_seven_days(self):
        shown = self.day0
        self.assertEqual(tip.should_show(4, shown, 7, 'complete', self.day0)[1], 'cadence')
        self.assertEqual(tip.should_show(5, shown, 7, 'complete', self.day0 + datetime.timedelta(days=6))[1], 'cadence')
        show, reason = tip.should_show(6, shown, 7, 'complete', self.day0 + datetime.timedelta(days=7))
        self.assertEqual((show, reason), (True, 'due'))

    def test_later_uses_thirty_days(self):
        shown = self.day0
        self.assertEqual(tip.should_show(9, shown, 30, 'complete', self.day0 + datetime.timedelta(days=7))[1], 'cadence')
        self.assertEqual(tip.should_show(9, shown, 30, 'complete', self.day0 + datetime.timedelta(days=29))[1], 'cadence')
        show, reason = tip.should_show(9, shown, 30, 'complete', self.day0 + datetime.timedelta(days=30))
        self.assertEqual((show, reason), (True, 'due'))

    def test_setup_blocks_even_after_three(self):
        show, reason = tip.should_show(5, None, 7, 'in_progress', self.day0)
        self.assertEqual((show, reason), (False, 'setup'))

    def test_missing_or_odd_setup_is_not_an_opt_out(self):
        for setup in (None, '', 'complete', 'off', 'never'):
            show, reason = tip.should_show(3, None, 7, setup, self.day0)
            self.assertEqual((show, reason), (True, 'due'), setup)

    def test_corrupt_cadence_stays_weekly(self):
        shown = self.day0
        for cadence in ('never', '0', '', None, '365', 'off', -1):
            show, reason = tip.should_show(3, shown, cadence, 'complete', self.day0 + datetime.timedelta(days=7))
            self.assertEqual((show, reason), (True, 'due'), cadence)
            self.assertEqual(
                tip.should_show(3, shown, cadence, 'complete', self.day0 + datetime.timedelta(days=6))[1],
                'cadence')

    def test_invalid_last_shown_does_not_block(self):
        show, reason = tip.should_show(3, 'tomorrow', 30, 'complete', self.day0)
        self.assertEqual((show, reason), (True, 'due'))
        show, reason = tip.should_show(3, datetime.date(2099, 1, 1), 30, 'complete', self.day0)
        self.assertEqual((show, reason), (True, 'due'))

class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.db = os.path.join(self.tmp.name, 'brain.db')
        self.env = os.environ.copy()
        self.env['MEM_DB'] = self.db

    def tearDown(self):
        self.tmp.cleanup()

    def run_tip(self, *args):
        p = subprocess.run(
            [sys.executable, os.path.join(HERE, 'tip.py'), *args],
            env=self.env, capture_output=True, text=True)
        return p

    def test_third_record_shows_then_week_then_later_is_monthly(self):
        day0 = datetime.date(2026, 11, 1)
        for n in (1, 2):
            got = parse(self.run_tip('record', '--date', day0.isoformat()).stdout)
            self.assertEqual(got['show'], 'no')
            self.assertEqual(got['reason'], 'count')
            self.assertEqual(got['conversions'], str(n))
            self.assertEqual(got['last_shown'], '')
        third = parse(self.run_tip('record', '--date', day0.isoformat()).stdout)
        self.assertEqual(third['show'], 'yes')
        self.assertEqual(third['reason'], 'due')
        self.assertEqual(third['conversions'], '3')
        self.assertEqual(third['cadence_days'], '7')
        self.assertEqual(third['last_shown'], day0.isoformat())
        self.assertEqual(third['setup'], 'complete')
        again = parse(self.run_tip('record', '--date', day0.isoformat()).stdout)
        self.assertEqual(again['show'], 'no')
        self.assertEqual(again['reason'], 'cadence')
        self.assertEqual(again['conversions'], '4')
        almost = day0 + datetime.timedelta(days=6)
        self.assertEqual(parse(self.run_tip('record', '--date', almost.isoformat()).stdout)['reason'], 'cadence')
        week = day0 + datetime.timedelta(days=7)
        nxt = parse(self.run_tip('record', '--date', week.isoformat()).stdout)
        self.assertEqual(nxt['show'], 'yes')
        self.assertEqual(nxt['last_shown'], week.isoformat())
        # Maybe later keeps the weekly cadence and does not count another conversion.
        snooze = parse(self.run_tip('later', '--date', week.isoformat()).stdout)
        self.assertEqual(snooze['show'], 'no')
        self.assertEqual(snooze['reason'], 'later')
        self.assertEqual(snooze['cadence_days'], '7')
        self.assertEqual(snooze['conversions'], '6')
        self.assertEqual(parse(self.run_tip('record', '--date', (week + datetime.timedelta(days=6)).isoformat()).stdout)['reason'], 'cadence')
        again_week = parse(self.run_tip('record', '--date', (week + datetime.timedelta(days=7)).isoformat()).stdout)
        self.assertEqual(again_week['show'], 'yes')
        self.assertEqual(again_week['cadence_days'], '7')

    def test_remind_monthly_and_dismiss_wait_thirty_days(self):
        day0 = datetime.date(2026, 11, 1)
        for _ in range(3):
            self.run_tip('record', '--date', day0.isoformat())
        # Dismissing without a button is the monthly command.
        dismissed = parse(self.run_tip('monthly', '--date', day0.isoformat()).stdout)
        self.assertEqual(dismissed['show'], 'no')
        self.assertEqual(dismissed['reason'], 'monthly')
        self.assertEqual(dismissed['cadence_days'], '30')
        self.assertEqual(dismissed['conversions'], '3')
        self.assertEqual(parse(self.run_tip('record', '--date', (day0 + datetime.timedelta(days=7)).isoformat()).stdout)['reason'], 'cadence')
        self.assertEqual(parse(self.run_tip('record', '--date', (day0 + datetime.timedelta(days=29)).isoformat()).stdout)['reason'], 'cadence')
        month = day0 + datetime.timedelta(days=30)
        shown = parse(self.run_tip('record', '--date', month.isoformat()).stdout)
        self.assertEqual(shown['show'], 'yes')
        self.assertEqual(shown['cadence_days'], '30')
        # Maybe later on a later visit returns to next week, even after a monthly gap.
        back = parse(self.run_tip('later', '--date', month.isoformat()).stdout)
        self.assertEqual(back['cadence_days'], '7')
        self.assertEqual(back['reason'], 'later')
        self.assertEqual(parse(self.run_tip('record', '--date', (month + datetime.timedelta(days=6)).isoformat()).stdout)['show'], 'no')
        nxt = parse(self.run_tip('record', '--date', (month + datetime.timedelta(days=7)).isoformat()).stdout)
        self.assertEqual(nxt['show'], 'yes')
        self.assertEqual(nxt['cadence_days'], '7')

    def test_setup_hides_the_prompt_and_does_not_burn_the_date(self):
        p = self.run_tip('setup-start')
        self.assertEqual(p.returncode, 0)
        self.assertEqual(parse(p.stdout)['setup'], 'in_progress')
        day = '2026-11-14'
        for _ in range(3):
            got = parse(self.run_tip('record', '--date', day).stdout)
            self.assertEqual(got['show'], 'no')
            self.assertEqual(got['reason'], 'setup')
            self.assertEqual(got['last_shown'], '')
        self.assertEqual(parse(self.run_tip('status').stdout)['conversions'], '3')
        done = parse(self.run_tip('setup-complete').stdout)
        self.assertEqual(done['setup'], 'complete')
        self.assertEqual(done['show'], 'no')
        # The next finished conversion, not the monthly check, is what may show it.
        self.assertEqual(parse(self.run_tip('status', '--date', day).stdout)['show'], 'no')
        shown = parse(self.run_tip('record', '--date', day).stdout)
        self.assertEqual(shown['show'], 'yes')
        self.assertEqual(shown['conversions'], '4')

    def test_status_and_unknown_commands_do_not_count(self):
        bad = self.run_tip('off')
        self.assertEqual(bad.returncode, 2)
        self.assertIn('record', bad.stderr)
        self.assertFalse(os.path.exists(self.db))
        nope = self.run_tip('record', '--never')
        self.assertEqual(nope.returncode, 2)
        self.assertFalse(os.path.exists(self.db))
        self.assertEqual(parse(self.run_tip('status').stdout)['conversions'], '0')
        self.assertEqual(parse(self.run_tip('status').stdout)['show'], 'no')
        con = sqlite3.connect(self.db)
        keys = [r[0] for r in con.execute('SELECT k FROM tip_state')]
        self.assertEqual(keys, [])
        self.assertNotIn('disabled', keys)
        self.assertNotIn('opt_out', keys)

    def test_db_error_does_not_fail_the_conversion(self):
        self.env['MEM_DB'] = os.path.join(self.tmp.name, 'missing-dir', 'brain.db')
        p = self.run_tip('record')
        self.assertEqual(p.returncode, 0)
        got = parse(p.stdout)
        self.assertEqual(got['show'], 'no')
        self.assertEqual(got['reason'], 'error')

    def test_existing_memory_rows_are_not_counted_or_changed(self):
        mem = os.path.join(ROOT, 'memory', 'mem')
        subprocess.run([mem, 'init'], env=self.env, check=True, capture_output=True, text=True)
        con = sqlite3.connect(self.db)
        self.assertIsNotNone(con.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='tip_state'").fetchone())
        con.close()
        subprocess.run([mem, 'fact', 'owner', 'default_destination', 'YouTube'],
                       env=self.env, check=True, capture_output=True, text=True)
        subprocess.run([mem, 'log', 'scan', 'looked at a playlist'],
                       env=self.env, check=True, capture_output=True, text=True)
        con = sqlite3.connect(self.db)
        con.execute("INSERT INTO log(kind, summary) VALUES('conversion', 'old')")
        con.commit()
        con.close()
        got = parse(self.run_tip('status').stdout)
        self.assertEqual(got['conversions'], '0')
        self.assertEqual(got['show'], 'no')
        # mem init created the table, and the owner's fact is still there after a count.
        parse(self.run_tip('record', '--date', '2026-11-01').stdout)
        con = sqlite3.connect(self.db)
        fact = con.execute(
            "SELECT value FROM fact WHERE subject='owner' AND predicate='default_destination' AND valid_to IS NULL"
        ).fetchone()
        logs = con.execute('SELECT COUNT(*) FROM log').fetchone()[0]
        self.assertEqual(fact[0], 'YouTube')
        self.assertEqual(logs, 2)
        self.assertEqual(int(con.execute("SELECT v FROM tip_state WHERE k='conversions'").fetchone()[0]), 1)

    def test_default_date_is_today(self):
        today = datetime.date.today().isoformat()
        for _ in range(3):
            got = parse(self.run_tip('record').stdout)
        self.assertEqual(got['show'], 'yes')
        self.assertEqual(got['last_shown'], today)

class CopyTests(unittest.TestCase):
    def read(self, *parts):
        with open(os.path.join(ROOT, *parts), encoding='utf-8') as f:
            return f.read()

    def test_prompt_and_links_are_verbatim(self):
        skill = self.read('skills', 'tip-prompt', 'SKILL.md')
        card = self.read('docs', 'tip-prompt.md')
        playlist = self.read('skills', 'playlist-conversion', 'SKILL.md')
        for text in (skill, card, playlist):
            self.assertIn(PROMPT, text)
            for _file, label, url in LINKS:
                self.assertIn(url, text)
                self.assertIn(label, text)
        self.assertIn(generate_qr.HANDLE, skill)
        self.assertIn(generate_qr.HANDLE, card)
        for label in generate_qr.BUTTONS:
            self.assertIn(label, skill)
            self.assertIn(label, card)
            self.assertIn(label, playlist)
        self.assertIn(generate_qr.LATER_REPLY, skill)
        self.assertIn(generate_qr.LATER_REPLY, card)
        self.assertIn(generate_qr.MONTHLY_REPLY, skill)
        self.assertIn(generate_qr.MONTHLY_REPLY, card)
        block = card.split('```json', 1)[1].split('```', 1)[0]
        self.assertLess(block.index('"Maybe later"'), block.index('"Remind me monthly"'))
        self.assertNotIn("Don't ask again", block)
        self.assertNotIn('opt out', block.lower())
        # First-run copy must not recite the tip ask.
        self.assertNotIn(PROMPT, self.read('skills', 'getting-started', 'SKILL.md'))

    def test_qr_pngs_encode_the_links(self):
        for name, _label, url in LINKS:
            path = os.path.join(HERE, 'qr', name)
            with open(path, 'rb') as f:
                magic = f.read(8)
            self.assertEqual(magic, b'\x89PNG\r\n\x1a\n', name)
            decoded = subprocess.run(['zbarimg', '-q', '--raw', path], capture_output=True, text=True)
            self.assertEqual(decoded.returncode, 0, decoded.stderr)
            self.assertEqual(decoded.stdout.strip(), url)

    def test_counter_script_does_not_use_the_network(self):
        src = self.read('tip', 'tip.py')
        self.assertNotIn('urllib', src)
        self.assertNotIn('subprocess', src)
        self.assertNotIn('socket', src)

    def test_weekly_update_stays_mandatory(self):
        text = self.read('routines', 'weekly-update-check.md')
        self.assertIn("can't be turned off", text)
        self.assertIn('always on', text)
        self.assertIn('no card to turn it off', text)
        version = self.read('VERSION').strip()
        self.assertEqual(version, '1.0.1')
        self.assertIn('## 1.0.1', self.read('CHANGELOG.md'))

if __name__ == '__main__':
    unittest.main()
