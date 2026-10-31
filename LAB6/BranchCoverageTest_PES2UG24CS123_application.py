import pytest
from course_registration import can_register, waitlist_position, late_fee


# ================= CAN REGISTER BRANCH TESTS =================

def test_invalid_student_status():
    with pytest.raises(ValueError):
        can_register("invalid", 10, 3, True)


def test_invalid_course_credits():
    with pytest.raises(ValueError):
        can_register("regular", 10, 0, True)


def test_negative_course_credits():
    with pytest.raises(ValueError):
        can_register("regular", 10, -2, True)


def test_prerequisites_not_met():
    assert can_register("regular", 10, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("probation", 15, 2, True) == "credit limit exceeded"


def test_regular_credit_limit_boundary():
    assert can_register("regular", 20, 4, True) == "registered"


def test_probation_credit_limit_boundary():
    assert can_register("probation", 14, 2, True) == "registered"


def test_honors_credit_limit_boundary():
    assert can_register("honors", 24, 4, True) == "registered"


# ================= WAITLIST BRANCH TESTS =================

def test_zero_capacity():
    with pytest.raises(ValueError):
        waitlist_position(10, 0, 0)


def test_negative_capacity():
    with pytest.raises(ValueError):
        waitlist_position(10, -5, 0)


def test_enrolled_below_capacity():
    assert waitlist_position(9, 10, 2) == 0


def test_enrolled_equals_capacity():
    assert waitlist_position(10, 10, 3) == 4


def test_waitlist_position_at_boundary():
    assert waitlist_position(10, 10, 9) == 10


def test_waitlist_limit_reached():
    assert waitlist_position(10, 10, 10) == -1


def test_waitlist_limit_exceeded():
    assert waitlist_position(10, 10, 12) == -1


# ================= LATE FEE BRANCH TESTS =================

def test_zero_late_days():
    assert late_fee(0, 10, False) == 0


def test_negative_late_days():
    assert late_fee(-1, 10, False) == 0


def test_late_fee_waiver():
    assert late_fee(10, 25, True) == 0


def test_seven_day_boundary():
    assert late_fee(7, 20, False) == 500


def test_eight_day_boundary():
    assert late_fee(8, 20, False) == 600


def test_credits_exactly_twenty():
    assert late_fee(8, 20, False) == 600


def test_credits_above_twenty():
    assert late_fee(8, 21, False) == 850


def test_fee_below_maximum():
    assert late_fee(10, 10, False) == 800


def test_fee_exceeds_maximum():
    assert late_fee(30, 21, False) == 2000


def test_fee_exactly_at_maximum():
    assert late_fee(22, 21, False) == 2000
