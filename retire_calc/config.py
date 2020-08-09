import os
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import AnyStr, Union

import yaml


class Config:
    default_config = {
        'birth_year': 1999,
        'life_span': 100,
        'retirement_age': 65,
        'cur_yearly_salary': 50000.0,
        'yearly_salary_increase_pct': .01,
        'yearly_investment_return_during_career': .07,
        'yearly_investment_return_during_retirement': .045,
        'upfront_investment': 0.0,
        'yearly_retirement_contribution_ratio': .15,
    }
    RETIREMENT_REDUCED_COST_FACTOR = .7

    def __init__(self, **kwargs):
        self.birth_year = kwargs.get('birth_year', Config.default_config['birth_year'])
        self.life_span = kwargs.get('life_span', Config.default_config['life_span'])
        self.retirement_age = kwargs.get('retirement_age', Config.default_config['retirement_age'])
        self.cur_yearly_salary = kwargs.get('cur_yearly_salary', Config.default_config['cur_yearly_salary'])
        self.yearly_salary_increase_pct = kwargs.get('yearly_salary_increase_pct',
                                                     Config.default_config['yearly_salary_increase_pct'])
        self.yearly_investment_return_during_career = kwargs.get('yearly_investment_return_during_career',
                                                                 Config.default_config[
                                                                     'yearly_investment_return_during_career'])
        self.yearly_investment_return_during_retirement = kwargs.get('yearly_investment_return_during_retirement',
                                                                     Config.default_config[
                                                                         'yearly_investment_return_during_retirement'])
        self.upfront_investment = kwargs.get('upfront_investment', Config.default_config['upfront_investment'])
        self.yearly_retirement_contribution_ratio = kwargs.get('yearly_retirement_contribution_ratio',
                                                               Config.default_config[
                                                                   'yearly_retirement_contribution_ratio'])
    def __repr__(self):
        return f'{self.__class__.__name__}(\n' \
               f'birth_year={self.birth_year}\n'\
                f'life_span={self.life_span}\n'\
                f'retirement_age={self.retirement_age}\n'\
                f'cur_yearly_salary={self.cur_yearly_salary}\n'\
                f'yearly_salary_increase_pct={self.yearly_salary_increase_pct}\n'\
                f'yearly_investment_return_during_career={self.yearly_investment_return_during_career}\n'\
                f'yearly_investment_return_during_retirement={self.yearly_investment_return_during_retirement}\n'\
                f'upfront_investment={self.upfront_investment}\n'\
                f'yearly_retirement_contribution_ratio={self.yearly_retirement_contribution_ratio}\n'\
               ')'

    @staticmethod
    def from_yaml(self, file_name='config.yaml'):
        with open(file_name, 'r') as f_read:
            d = yaml.safe_load(f_read)

            birth_year = d.get('birth_year', Config.default_config['birth_year'])
            life_span = d.get('life_span', Config.default_config['life_span'])
            retirement_age = d.get('retirement_age', Config.default_config['retirement_age'])
            cur_yearly_salary = d.get('cur_yearly_salary', Config.default_config['cur_yearly_salary'])
            yearly_salary_increase_pct = d.get('yearly_salary_increase_pct',
                                               Config.default_config['yearly_salary_increase_pct'])
            yearly_investment_return_during_career = d.get('yearly_investment_return_during_career',
                                                           Config.default_config[
                                                               'yearly_investment_return_during_career'])
            yearly_investment_return_during_retirement = d.get('yearly_investment_return_during_retirement',
                                                               Config.default_config[
                                                                   'yearly_investment_return_during_retirement'])
            upfront_investment = d.get('upfront_investment', Config.default_config['upfront_investment'])
            yearly_retirement_contribution_ratio = d.get('yearly_retirement_contribution_ratio',
                                                         Config.default_config[
                                                             'yearly_retirement_contribution_ratio'])
            return Config(
                birth_year=birth_year,
                life_span=life_span,
                retirement_age=retirement_age,
                cur_yearly_salary=cur_yearly_salary,
                yearly_salary_increase_pct=yearly_salary_increase_pct,
                yearly_investment_return_during_career=yearly_investment_return_during_career,
                yearly_investment_return_during_retirement=yearly_investment_return_during_retirement,
                upfront_investment=upfront_investment,
                yearly_retirement_contribution_ratio=yearly_retirement_contribution_ratio
            )


    def overwrite_with_cli_args(self, cli_args: Union[Namespace]):
        for k in self.default_config:
            if hasattr(self, k) and hasattr(cli_args, k):
                cli_arg_val = getattr(cli_args, k)
                if cli_arg_val is not None:
                    type1 = type(getattr(self, k))
                    setattr(self, k, type1(cli_arg_val))

    @property
    def years_alive_post_retirement(self):
        return self.life_span - self.retirement_age

    def get_yearly_retirement_contribution_gen(self):
        p = self.cur_yearly_salary
        import itertools
        growth_rate = self.yearly_salary_increase_pct + 1

        return (self.yearly_retirement_contribution_ratio * p * (growth_rate ** year_num) for year_num in itertools.count(0))

    @property
    def years_until_retirement(self):
        return self.retirement_year - datetime.now().year

    @property
    def yearly_retirement_stipend(self):
        return self.cur_yearly_salary * Config.RETIREMENT_REDUCED_COST_FACTOR

    @property
    def retirement_year(self):
        return self.birth_year + self.retirement_age

    @classmethod
    def write_default_config(cls, filepath: Union[AnyStr, Path]):
        with open(filepath, 'w') as f_write:
            f_write.write(yaml.dump(cls.default_config))
