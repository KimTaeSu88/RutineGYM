import unittest

from routine_generator import RoutineDay, generate_workout_routine


class WorkoutRoutineTests(unittest.TestCase):
    def test_generate_returns_requested_days(self):
        routine = generate_workout_routine(goal="근력", days_per_week=4)

        self.assertEqual(4, len(routine))
        self.assertTrue(all(isinstance(day, RoutineDay) for day in routine))
        self.assertTrue(all(len(day.exercises) == 3 for day in routine))

    def test_goal_template_is_applied(self):
        routine = generate_workout_routine(goal="근력", days_per_week=1)

        self.assertEqual(["스쿼트", "벤치프레스", "데드리프트"], routine[0].exercises)

    def test_invalid_goal_raises(self):
        with self.assertRaises(ValueError):
            generate_workout_routine(goal="벌크업", days_per_week=3)

    def test_invalid_days_raises(self):
        with self.assertRaises(ValueError):
            generate_workout_routine(goal="유지", days_per_week=0)


if __name__ == "__main__":
    unittest.main()
