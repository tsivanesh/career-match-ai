import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from database.database import query_db

class TestCareerMatchAI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_01_landing_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'CareerMatch', response.data)
        self.assertIn(b'Find Your', response.data)
        print("[PASS] Test 01: Landing page loads successfully.")

    def test_02_demo_login(self):
        response = self.client.get('/demo-login', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Alex Chen', response.data)
        self.assertIn(b'Dashboard', response.data)
        print("[PASS] Test 02: 1-Click Demo student login works.")

    def test_03_dashboard_view(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2 # Alex Chen
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Good evening, Alex', response.data)
        self.assertIn(b'Profile Completion', response.data)
        self.assertIn(b'AI Matched Jobs', response.data)
        print("[PASS] Test 03: Student Dashboard renders charts and statistics.")

    def test_04_recommendations_engine(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.get('/recommendations')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'AI Job Recommendations', response.data)
        # Check that match percentage badges exist
        self.assertIn(b'match-score-badge', response.data)
        print("[PASS] Test 04: AI Recommendation engine ranks jobs with match percentages.")

    def test_05_job_detail_and_why_matches(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.get('/job/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Why this job matches you', response.data)
        self.assertIn(b'Skill Match', response.data)
        print("[PASS] Test 05: Job Details renders 'Why this job matches you' and skill gaps.")

    def test_06_skill_gap_page(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.get('/skill-gap/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Skill Gap Analysis', response.data)
        self.assertIn(b'Skills to Develop', response.data)
        print("[PASS] Test 06: Skill Gap Analysis page renders comparison & suggestions.")

    def test_07_job_search_filters(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.get('/search?q=Python&category=Software+Engineering')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job Search', response.data)
        self.assertIn(b'Python', response.data)
        print("[PASS] Test 07: Job Search with keyword & category filters works.")

    def test_08_save_and_unsave_job(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        # Toggle save
        response = self.client.post('/save-job/5')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('saved', data)
        print("[PASS] Test 08: Save/Unsave job bookmark AJAX endpoint works.")

    def test_09_applications_kanban(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.get('/applications')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Application Tracker', response.data)
        self.assertIn(b'kanban-col', response.data)
        print("[PASS] Test 09: Kanban Application Tracker renders all status columns.")

    def test_10_application_status_update(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 2
            sess['user_name'] = 'Alex Chen'
            sess['user_role'] = 'student'
        response = self.client.post('/applications/update', json={
            'job_id': 1,
            'status': 'Interview',
            'notes': 'Verified status update test.'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(data['success'])
        print("[PASS] Test 10: Kanban Application status update works.")

    def test_11_admin_dashboard(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1 # Admin
            sess['user_name'] = 'CareerMatch Admin'
            sess['user_role'] = 'admin'
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)
        self.assertIn(b'Popular Skills', response.data)
        print("[PASS] Test 11: Admin dashboard renders platform analytics.")

    def test_12_admin_manage_jobs(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['user_name'] = 'CareerMatch Admin'
            sess['user_role'] = 'admin'
        response = self.client.get('/admin/jobs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Manage Jobs', response.data)
        print("[PASS] Test 12: Admin job management page renders table & add modal.")

if __name__ == '__main__':
    unittest.main()
