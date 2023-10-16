import sys
import os
#import getch
import tkinter as tk
from sympy import pprint, init_printing
import sympy.physics.units as u
init_printing(use_unicode=True)


class unit_convert:
    hectometer = u.Quantity('hm')
    hectometers = hm = hectometer
    hectometer.set_global_relative_scale_factor(100, u.m)

    decameter = u.Quantity('dam')
    dam = decameters = decameter
    decameter.set_global_relative_scale_factor(10, u.m)

    angstrom = u.Quantity('A')
    angstroms = A = angstrom
    angstrom.set_global_relative_scale_factor(10*-11, u.m)

    furlong = u.Quantity('fur')
    furlongs = fur = furlong
    furlong.set_global_relative_scale_factor(201.168, u.m)

    chain = u.Quantity('ch')
    chains = ch = chain
    chain.set_global_relative_scale_factor(20.1168, u.m)

    rod = u.Quantity('rd')
    rods = rd = rod
    rod.set_global_relative_scale_factor(5.0292, u.m)

    link = u.Quantity('li')
    links = lk = link
    link.set_global_relative_scale_factor(0.201168, u.m)

    hand = u.Quantity('hh')
    hands = hh = hand
    hand.set_global_relative_scale_factor(0.1016, u.m)

    thou = u.Quantity('th')
    thous = th = thou
    thou.set_global_relative_scale_factor(0.0000254, u.m)

    cable = u.Quantity('cbl')
    cables = cbl = cable
    cable.set_global_relative_scale_factor(185.2, u.m)

    fathom = u.Quantity('ftm')
    fathoms = ftm = fathom
    fathom.set_global_relative_scale_factor(1.8288, u.m)

    manual_length_check_list = ['hectometer', 'hectometers', 'hm',
                                'decameter', 'decameters', 'dam',
                                'angstrom', 'angstroms', 'A',
                                'furlong', 'furlongs', 'fur',
                                'chain', 'chains', 'ch',
                                'rod', 'rods', 'rd',
                                'link', 'links', 'li',
                                'hand', 'hands', 'hh',
                                'thou', 'thous', 'th',
                                'cable', 'cables', 'cbl',
                                'fathom', 'fathoms', 'ftm']

    def length(init_unit, final_unit, number, rational_return: bool):
        if init_unit in u.find_unit("length"):
            if final_unit in u.find_unit("length"):
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit)).n()
            elif final_unit in unit_convert.manual_length_check_list:
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(unit_convert, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(unit_convert, final_unit)).n()
        elif init_unit in unit_convert.manual_length_check_list:
            if final_unit in u.find_unit("length"):
                if rational_return:
                    return u.convert_to(number * getattr(unit_convert, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(unit_convert, init_unit), getattr(u, final_unit)).n()
            elif final_unit in unit_convert.manual_length_check_list:
                if rational_return:
                    return u.convert_to(number * getattr(unit_convert, init_unit), getattr(unit_convert, final_unit))
                else:
                    return u.convert_to(number * getattr(unit_convert, init_unit), getattr(unit_convert, final_unit)).n()

    def area(init_unit, final_unit, number, rational_return: bool):
        init_unit = init_unit[:len(init_unit) - 3]
        final_unit = final_unit[:len(final_unit) - 3]
        for i in range(2):
            sub = unit_convert.length(init_unit, final_unit, number, False)
            number = float(list({atom for atom in sub.atoms() if atom.is_number})[0])
        sub = number * getattr(u, final_unit)**2
        return sub

    def valume(init_unit, final_unit, number, rational_return: bool):
        init_unit = init_unit[:len(init_unit) - 3]
        final_unit = final_unit[:len(final_unit) - 3]
        for i in range(3):
            sub = unit_convert.length(init_unit, final_unit, number, False)
            number = float(list({atom for atom in sub.atoms() if atom.is_number})[0])
        sub = number * getattr(u, final_unit)**3
        return sub

    sympy_mass_checker_list = ['g', 't', 'Da', 'kg', 'mg', 'ug', 'amu',
                               'mmu', 'amus', 'gram', 'mmus', 'grams',
                               'pound', 'tonne', 'dalton', 'pounds',
                               'kilogram', 'kilograms', 'microgram',
                               'milligram', 'metric_ton', 'micrograms',
                               'milligrams', 'planck_mass', 'milli_mas',
                               's_unit', 'atomic_mass_unit', 'atomic_mass_constant']

    def mass(init_unit, final_unit, number, rational_return: bool):
        if init_unit in u.find_unit("mass"):
            if final_unit in u.find_unit("mass"):
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit)).n()

    def velocity(init_unit, final_unit, number, rational_return: bool):
        init_unit_numerator = init_unit.split('/')[0]
        init_unit_denominator = init_unit.split('/')[1]
        final_unit_numerator = final_unit.split('/')[0]
        final_unit_denominator = final_unit.split('/')[1]
        if rational_return:
            return u.convert_to(number * (getattr(u, init_unit_numerator) / getattr(u, init_unit_denominator)),
                                         (getattr(u, final_unit_numerator) / getattr(u, final_unit_denominator)))
        else:
            return u.convert_to(number * (getattr(u, init_unit_numerator) / getattr(u, init_unit_denominator)),
                                         (getattr(u, final_unit_numerator) / getattr(u, final_unit_denominator))).n()

    def pressure(init_unit, final_unit, number, rational_return):
        if init_unit in u.find_unit("pressure"):
            if final_unit in u.find_unit("pressure"):
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit)).n()

    def energy(init_unit, final_unit, number, rational_return):
        if init_unit in u.find_unit("energy"):
            if final_unit in u.find_unit("energy"):
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit)).n()

    def power(init_unit, final_unit, number, rational_return):
        if init_unit in u.find_unit("power"):
            if final_unit in u.find_unit("power"):
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit)).n()

    def temperature(init_unit, final_unit, number, rational_return):
        if init_unit in u.find_unit("temperature"):
            if final_unit in u.find_unit("temperature"):
                if rational_return:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit))
                else:
                    return u.convert_to(number * getattr(u, init_unit), getattr(u, final_unit)).n()


class cli_interface:
    light_gray = "#F5F5F5"
    def live_output(init_unit, final_unit):
        current_str = ''
        output = ''
        while True:
            os.system("clear")
            print(f"output: {output}\ninput: {current_str}", end='')
            live_input: str = getch.getch()

            if live_input == "\x7f":
                current_str = current_str[:-1]
            elif live_input in ("\n", "\r", "\r\n", "\x04"):
                break
            else:
                current_str += live_input
            if current_str != '':
                output = unit_convert.length(init_unit, final_unit, int(current_str), False)
            else:
                output = ''





