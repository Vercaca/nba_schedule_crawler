import logging

from parsers import ParserHelper
from entity import ScheduleRow

logger = logging.getLogger(__name__)


CLS_SCHEDULE_CONTENT = 'schedule-content'
CLS_SCHEDULE_GAMES = 'schedule-games'
CLS_SCHEDULE_GAME = 'schedule-game'
CLS_SCHEDULE_GAME_CONTENT = f'{CLS_SCHEDULE_GAME}__content'
CLS_SCHEDULE_GAME_STATUS = f'{CLS_SCHEDULE_GAME}__status'
CLS_SCHEDULE_GAME_CARD = f'{CLS_SCHEDULE_GAME}__card'
CLS_SCHEDULE_GAME_SEASON = f'{CLS_SCHEDULE_GAME}__season'

CLS_SCHEDULE_GAME_TEAM = f'{CLS_SCHEDULE_GAME}__team'
CLS_SCHEDULE_HOME_TEAM = f'{CLS_SCHEDULE_GAME_TEAM}--htm'
CLS_SCHEDULE_VISIT_TEAM = f'{CLS_SCHEDULE_GAME_TEAM}--vtm'


class SchedulePageParser(ParserHelper):
    @classmethod
    def parse_game_list(cls, soup):
        games = []
        date_sections = soup.find_all('section', class_=CLS_SCHEDULE_CONTENT)
        # print(len(date_sections))
        for date_section in date_sections:
            date_text = date_section['data-game-day']
            date_acticles = date_section.find_all('article')
            for acticle in date_acticles:
                game_id = acticle['id']
                article = acticle.find('div', class_=CLS_SCHEDULE_GAME_CONTENT)
                game_status = article.find('div', class_=CLS_SCHEDULE_GAME_STATUS)

                game_time = game_status.find_all('span')[0].text
                game_season = game_status.find('span', class_=CLS_SCHEDULE_GAME_SEASON).text

                game_h_team, game_v_team = cls._get_team_names_from_article(article)

                game = ScheduleRow(id=game_id, date=date_text, time=game_time, season=game_season,
                                   h_team=game_h_team, v_team=game_v_team)
                # print(game)
                games.append(game)
            # print('-'*100)
        return games

    @staticmethod
    def _get_team_names_from_article(article):
        game_card = article.find('div', class_=CLS_SCHEDULE_GAME_CARD)
        try:
            game_h_team = game_card.find('tr', class_=CLS_SCHEDULE_HOME_TEAM).th.a .text
        except AttributeError:
            game_h_team = game_card.find('tr', class_=CLS_SCHEDULE_HOME_TEAM).th.span.text

        try:
            game_v_team = game_card.find('tr', class_=CLS_SCHEDULE_VISIT_TEAM).th.a .text
        except AttributeError:
            game_v_team = game_card.find('tr', class_=CLS_SCHEDULE_VISIT_TEAM).th.span.text
        return game_h_team, game_v_team
