import unittest
from datetime import date

from app.models.employee import Employee
from app.models.leave import LeaveRequest
from app.services.attendance import (
    approved_leave_by_employee_name,
    calculate_attendance,
    is_employee_scheduled_for_date,
)


class AttendanceRuleTests(unittest.TestCase):
    def make_payload(self, **overrides):
        payload = {
            "shift_start": "09:00",
            "shift_end": "18:00",
            "grace_minutes": 0,
            "clock_in": "09:00",
            "clock_out": "18:00",
            "break_out": None,
            "break_in": None,
        }
        payload.update(overrides)
        return payload

    def test_present_employee_on_schedule(self):
        result = calculate_attendance(self.make_payload())

        self.assertEqual(result["status"], "Present")
        self.assertEqual(result["worked_hours"], 9)
        self.assertEqual(result["payable_hours"], 9)

    def test_grace_period_is_removed_from_late_minutes(self):
        result = calculate_attendance(
            self.make_payload(clock_in="09:10", grace_minutes=5)
        )

        self.assertEqual(result["status"], "Late")
        self.assertEqual(result["late_minutes"], 5)

    def test_undertime_is_detected(self):
        result = calculate_attendance(self.make_payload(clock_out="17:30"))

        self.assertEqual(result["status"], "Undertime")
        self.assertEqual(result["undertime_minutes"], 30)

    def test_missing_clock_is_incomplete(self):
        result = calculate_attendance(self.make_payload(clock_out=""))

        self.assertEqual(result["status"], "Incomplete")
        self.assertEqual(result["worked_hours"], 0)
        self.assertEqual(result["payable_hours"], 0)

    def test_overnight_shift_uses_next_day_clock_out(self):
        result = calculate_attendance(
            self.make_payload(
                shift_start="22:00",
                shift_end="06:00",
                clock_in="22:00",
                clock_out="06:00",
            )
        )

        self.assertEqual(result["status"], "Present")
        self.assertEqual(result["worked_hours"], 8)
        self.assertEqual(result["night_diff_minutes"], 480)

    def test_break_is_deducted_from_worked_and_payable_hours(self):
        result = calculate_attendance(
            self.make_payload(break_out="12:00", break_in="13:00")
        )

        self.assertEqual(result["worked_hours"], 8)
        self.assertEqual(result["payable_hours"], 8)

    def test_overtime_is_tracked_but_not_automatically_payable(self):
        result = calculate_attendance(self.make_payload(clock_out="20:00"))

        self.assertEqual(result["overtime_minutes"], 120)
        self.assertEqual(result["worked_hours"], 11)
        self.assertEqual(result["payable_hours"], 9)

    def test_invalid_same_day_clock_order_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "earlier than clock in"):
            calculate_attendance(self.make_payload(clock_in="18:00", clock_out="09:00"))

    def test_active_employee_is_scheduled_on_configured_workday(self):
        employee = Employee(
            employee_code="EMP-T1",
            first_name="Test",
            last_name="Employee",
            email="test1@example.com",
            department="Operations",
            position="Staff",
            employment_status="Regular",
            account_status="Active",
            work_days="mon,tue,wed,thu,fri",
        )

        self.assertTrue(is_employee_scheduled_for_date(employee, date(2026, 7, 13)))

    def test_active_employee_is_not_scheduled_on_rest_day(self):
        employee = Employee(
            employee_code="EMP-T2",
            first_name="Test",
            last_name="Employee",
            email="test2@example.com",
            department="Operations",
            position="Staff",
            employment_status="Regular",
            account_status="Active",
            work_days="mon,tue,wed,thu,fri",
        )

        self.assertFalse(is_employee_scheduled_for_date(employee, date(2026, 7, 12)))

    def test_approved_leave_is_matched_for_selected_date(self):
        requests = [
            LeaveRequest(
                request_id="LV-T1",
                employee_name="Test Employee",
                leave_type="Vacation Leave",
                start_date="2026-07-13",
                end_date="2026-07-15",
                reason="Planned",
                approver="HR",
                status="Approved",
            )
        ]

        leaves = approved_leave_by_employee_name(requests, date(2026, 7, 14))

        self.assertIn("test employee", leaves)
        self.assertEqual(leaves["test employee"].leave_type, "Vacation Leave")

    def test_pending_leave_is_not_treated_as_on_leave(self):
        requests = [
            LeaveRequest(
                request_id="LV-T2",
                employee_name="Test Employee",
                leave_type="Sick Leave",
                start_date="2026-07-13",
                end_date="2026-07-13",
                reason="Medical",
                approver="HR",
                status="Pending",
            )
        ]

        leaves = approved_leave_by_employee_name(requests, date(2026, 7, 13))

        self.assertNotIn("test employee", leaves)


if __name__ == "__main__":
    unittest.main()
