import unittest

from app.models.user import User, UserRole
from app.services.audit import actor_label


class AuditLogTests(unittest.TestCase):
    def test_actor_label_prefers_full_name(self):
        user = User(
            username="hr",
            full_name="HR Admin",
            email="hr@example.com",
            hashed_password="hash",
            role=UserRole.hr_admin,
        )

        self.assertEqual(actor_label(user), "HR Admin")

    def test_actor_label_uses_system_for_missing_user(self):
        self.assertEqual(actor_label(None), "System")


if __name__ == "__main__":
    unittest.main()
