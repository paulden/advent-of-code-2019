from fuel_requirement import compute_fuel_requirement, compute_total_fuel_requirement_for_module


def test_compute_fuel_requirement_should_return_0_when_mass_is_0():
    fuel_required = compute_fuel_requirement(mass=0)
    assert fuel_required == 0


def test_compute_fuel_requirement_should_return_4_when_mass_is_12():
    fuel_required = compute_fuel_requirement(mass=12)
    assert fuel_required == 2


def test_compute_fuel_requirement_should_return_4_when_mass_is_14():
    fuel_required = compute_fuel_requirement(mass=14)
    assert fuel_required == 2


def test_compute_fuel_requirement_should_return_654_when_mass_is_1969():
    fuel_required = compute_fuel_requirement(mass=1969)
    assert fuel_required == 654


def test_compute_fuel_requirement_should_return_33583_when_mass_is_100756():
    fuel_required = compute_fuel_requirement(mass=100756)
    assert fuel_required == 33583


def test_compute_total_fuel_requirement_for_module_should_return_0_when_module_mass_is_0():
    total_fuel_required = compute_total_fuel_requirement_for_module(mass=0)
    assert total_fuel_required == 0


def test_compute_total_fuel_requirement_for_module_should_return_2_when_module_mass_is_14():
    total_fuel_required = compute_total_fuel_requirement_for_module(mass=14)
    assert total_fuel_required == 2


def test_compute_total_fuel_requirement_for_module_should_return_966_when_module_mass_is_1969():
    total_fuel_required = compute_total_fuel_requirement_for_module(mass=1969)
    assert total_fuel_required == 966


def test_compute_total_fuel_requirement_for_module_should_return_50346_when_module_mass_is_100756():
    total_fuel_required = compute_total_fuel_requirement_for_module(mass=100756)
    assert total_fuel_required == 50346
