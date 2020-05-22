import os
from datetime import datetime
from typing import Union, AnyStr
from pathlib import Path

import yaml


class Config:
    default_config = {
        'birth_year': 2000,
        'life_span': 100,
        'retirement_age': 65,
        'cur_yearly_salary': 50000,
        'yearly_salary_increase_pct': .01,
        'yearly_investment_return_during_career': .07,
        'yearly_investment_return_during_retirement': .045,
        'upfront_investment': 0,
        'yearly_retirement_contribution_ratio': .15,
    }

    def __init__(self, file_name='config.yaml'):
        if os.path.isfile(file_name):
            with open(file_name, 'r') as f_read:
                d = yaml.safe_load(f_read)

                self.birth_year = d.get('birth_year', Config.default_config['birth_year'])
                self.life_span = d.get('life_span', Config.default_config['life_span'])
                self.retirement_age = d.get('retirement_age', Config.default_config['retirement_age'])
                self.cur_yearly_salary = d.get('cur_yearly_salary', Config.default_config['cur_yearly_salary'])
                self.yearly_salary_increase_pct = d.get('yearly_salary_increase_pct', Config.default_config['yearly_salary_increase_pct'])
                self.yearly_investment_return_during_career = d.get('yearly_investment_return_during_career', Config.default_config['yearly_investment_return_during_career'])
                self.yearly_investment_return_during_retirement = d.get('yearly_investment_return_during_retirement', Config.default_config['yearly_investment_return_during_retirement'])
                self.upfront_investment = d.get('upfront_investment', Config.default_config['upfront_investment'])
                self.yearly_retirement_contribution_ratio = d.get('yearly_retirement_contribution_ratio', Config.default_config['yearly_retirement_contribution_ratio'])
        else:
            self.birth_year = Config.default_config['birth_year']
            self.life_span = Config.default_config['life_span']
            self.retirement_age = Config.default_config['retirement_age']
            self.cur_yearly_salary = Config.default_config['cur_yearly_salary']
            self.yearly_salary_increase_pct = Config.default_config['yearly_salary_increase_pct']
            self.yearly_investment_return_during_career = Config.default_config['yearly_investment_return_during_career']
            self.yearly_investment_return_during_retirement = Config.default_config['yearly_investment_return_during_retirement']
            self.upfront_investment = Config.default_config['upfront_investment']
            self.yearly_retirement_contribution_ratio = Config.default_config['yearly_retirement_contribution_ratio']

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
        return self.cur_yearly_salary * .7

    @property
    def retirement_year(self):
        return self.birth_year + self.retirement_age

    @classmethod
    def write_default_config(cls, filepath:Union[AnyStr, Path]):
        with open(filepath, 'w') as f_write:
            f_write.write(yaml.dump(cls.default_config))
