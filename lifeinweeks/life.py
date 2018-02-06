"""Life Calendar

inspired by Tim Urban of Wait But Why
https://waitbutwhy.com/2014/05/life-weeks.html

"""

import ui


w, h = ui.get_screen_size()

NUM_WEEKS = 52
NUM_YEARS = 30
SIZE = 7
SIZE = w / NUM_WEEKS


class LifeView(ui.View):
  APP_NAME = 'Life Calendar'
  
  def __init__(self):
    self.main_view = self._create_main_view()
    self._init_weeks()
    self.navi_view = self._show_app()
  
  def _create_main_view(self):
    scroll = ui.ScrollView()
    scroll.name = self.APP_NAME
    scroll.width = w
    scroll.height = h
    scroll.background_color = 'white'
    scroll.content_size = (w, NUM_YEARS * SIZE + 100)
    scroll.always_bounce_vertical = True
    scroll.always_bounce_horizontal = True
    return scroll
  
  def _init_weeks(self):
    for week in range(NUM_WEEKS):
      for year in range(NUM_YEARS):
        button = ui.Button()
        button.action = button_action(week+1, year)
        button.border_width = 1
        button.border_color = 'lightgrey'
        # (x, y, width, height)
        button.frame = (
          SIZE * week,
          SIZE * year,
          SIZE,
          SIZE
        )
        self.main_view.add_subview(button)
    
  def _show_app(self):
    nv = ui.NavigationView(self.main_view)
    nv.name = 'Navi View'
    btni_close = ui.ButtonItem(title="Close", action=lambda s: nv.close())
    self.main_view.left_button_items = [btni_close]
    nv.present('sheet', hide_title_bar=True)
    return nv


def button_action(week, year):
  def button_tapped(sender):
    v = ui.load_view('lifeweek')
    txt = 'week {}, year {}'.format(week, year)
    v['lbl_weekyear'].text = txt
    v['btn_wprev'].action = button_action(week-1, year)
    v['btn_wnext'].action = button_action(week+1, year)
    v['btn_yprev'].action = button_action(week, year-1)
    v['btn_ynext'].action = button_action(week, year+1)
    nv = sender.navigation_view
    nv.push_view(v)
    
    def home_tapped(sender):
      v.pop_view()
    
    btni_home = ui.ButtonItem(title='Overview')
    btni_home.action = home_tapped
    v.right_button_items = [btni_home]
  return button_tapped


def main():
  LifeView()

if __name__ == '__main__':
  main()
