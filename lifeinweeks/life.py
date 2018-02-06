"""Life Calendar

inspired by Tim Urban of Wait But Why
https://waitbutwhy.com/2014/05/life-weeks.html

"""

import ui
import dialogs


NUM_WEEKS = 52
NUM_YEARS = 30
#SIZE = w / NUM_WEEKS


class LifeView(ui.View):
  APP_NAME = 'Life Calendar'
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.BTN_SIZE = self.width / NUM_WEEKS
    self.main_view = self.create_main_view()
    self.navi_view = self.create_navi_view()
    self.init_weeks(NUM_WEEKS, NUM_YEARS)
  
  def create_main_view(self):
    scroll = ui.ScrollView()
    scroll.name = self.APP_NAME
    scroll.width = self.width
    scroll.height = self.height
    scroll.background_color = 'white'
    scroll.content_size = (
      self.width,
      NUM_YEARS * self.BTN_SIZE + 100
    )
    scroll.always_bounce_vertical = True
    scroll.always_bounce_horizontal = True
    
    close = lambda s: self.close()
    btni_close = ui.ButtonItem(title="Close", action=close)
    scroll.left_button_items = [btni_close]
    
    def settings(sender):
      dlg = dialogs.form_dialog(title='Settings',
        fields=[
          {
            'type': 'text',
            'title': 'Name',
          },
          {
            'type': 'date',
            'title': 'Date of birth'
          }
        ]
      )
      print(dlg)
    
    btni_settings = ui.ButtonItem(title='Settings', action=settings)
    scroll.right_button_items =[btni_settings]
    
    return scroll
  
  def create_navi_view(self):
    nv = ui.NavigationView(self.main_view)
    nv.name = 'Navi View'
    nv.frame = self.frame
    self.add_subview(nv)
    return nv
  
  @ui.in_background
  def init_weeks(self, weeks, years):
    for year in range(years):
      for week in range(weeks):
        button = ui.Button()
        button.action = self._week_action(week+1, year)
        button.border_width = 1
        button.border_color = 'lightgrey'
        # (x, y, width, height)
        button.frame = (
          self.BTN_SIZE * week,
          self.BTN_SIZE * year,
          self.BTN_SIZE,
          self.BTN_SIZE
        )
        self.main_view.add_subview(button)

  def _week_action(self, week, year):
    def button_tapped(sender):
      v = ui.load_view('lifeweek')
      v.name = 'Week {}'.format(week * year)
      txt = 'week {}, year {}'.format(week, year)
      v['lbl_weekyear'].text = txt
      v['btn_wprev'].action = self._week_action(week-1, year)
      v['btn_wnext'].action = self._week_action(week+1, year)
      v['btn_yprev'].action = self._week_action(week, year-1)
      v['btn_ynext'].action = self._week_action(week, year+1)
      nv = sender.navigation_view
      nv.push_view(v)
      
      def home_tapped(sender):
        self.navi_view.pop_view()
      
      btni_home = ui.ButtonItem(title='Overview')
      btni_home.action = home_tapped
      v.right_button_items = [btni_home]
    return button_tapped


if __name__ == '__main__':
  w, h = ui.get_screen_size()
  f = (0, 0, w, h)
  view = LifeView(frame=f)
  view.present(style='sheet', hide_title_bar=True)

