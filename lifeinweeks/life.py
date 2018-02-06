"""Life Calendar

inspired by Tim Urban of Wait But Why
https://waitbutwhy.com/2014/05/life-weeks.html

"""

import ui
import dialogs
import shelve
import datetime
from dateutil import rrule


NUM_WEEKS = 52
NUM_YEARS = 30
DB_FILE = 'data/storage.db'


class LifeView(ui.View):
  APP_NAME = 'Life Calendar'
  
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.BTN_SIZE = self.width / NUM_WEEKS
    self.settings = self.load('settings')
    
    self.main_view = self.create_main_view()
    self.navi_view = self.create_navi_view()
    self.personalize(self.settings)
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
    
    btni_settings = ui.ButtonItem(
      title='Settings',
      action=self.settings_action
    )
    scroll.right_button_items = [
      btni_settings,
    ]
    return scroll
  
  def personalize(self, profile):
    name = profile.get('name', None)
    dob = profile.get('dob', None)
    
    if name and dob:
      lbl_name = ui.Label(
        name='lbl_name',
        text=name,
        font=('<system-bold>', 30),
        x=10,
        width=self.width/2,
      )
      lbl_dob = ui.Label(
        name='lbl_dob',
        text=dob.strftime("%d.%m.%Y"),
        font=('<system-bold>', 30),
        x=self.width/2+10,
        width=self.width/2,
      )
      
      for sv in self.main_view.subviews:
        if sv.name in ('lbl_name', 'lbl_dob'):
          self.main_view.remove_subview(sv)
      
      self.main_view.add_subview(lbl_name)
      self.main_view.add_subview(lbl_dob)
  
  def settings_action(self, sender):
    settings = dialogs.form_dialog(title='Settings',
      fields=[
        {
          'type': 'text',
          'title': 'Name',
          'key': 'name',
          'value': self.settings.get('name', ''),
        },
        {
          'type': 'date',
          'title': 'Date of birth',
          'key': 'dob',
          'value': self.settings.get('dob', datetime.datetime.today()),
        }
      ]
    )
    # None if form is not saved
    if settings:
      self.save('settings', settings)
      self.settings = settings
      self.personalize(self.settings)
      dialogs.hud_alert('Saved')
  
  def save(self, key, data):
    with shelve.open(DB_FILE) as db:
      db[key] = data
  
  def load(self, key):
    with shelve.open(DB_FILE) as db:
      data = db.get(key, dict())
    return data
  
  def create_navi_view(self):
    nv = ui.NavigationView(self.main_view)
    nv.name = 'Navi View'
    nv.frame = self.frame
    self.add_subview(nv)
    return nv
  
  @ui.in_background
  def init_weeks(self, weeks, years):
    dob = self.settings['dob']
    curr_week = datetime.datetime.today()
    past_weeks = delta_between_dates(
      rrule.WEEKLY, dob, curr_week)
    
    for year in range(years):
      for week in range(weeks):
        button = ui.Button()
        button.action = self._week_action(week+1, year)
        button.border_width = 1
        
        week_counter = week + NUM_WEEKS * year
        if week_counter == past_weeks:
          button.border_width = 3
          button.border_color = 'red'
        else:
          button.border_color = 'lightgrey'
        
        # (x, y, width, height)
        button.frame = (
          self.BTN_SIZE * week,
          self.BTN_SIZE * year + 100,
          self.BTN_SIZE,
          self.BTN_SIZE
        )
        self.main_view.add_subview(button)

  def _week_action(self, week, year):
    def button_tapped(sender):
      v = ui.load_view('lifeweek')
      v.name = 'Week {}'.format(week + NUM_WEEKS * year)
      txt = 'week {}, year {}'.format(week, year)
      week_start = self.settings.get('dob', None)
      
      v['lbl_weekyear'].text = txt
      v['lbl_date'].text = week_start.strftime("%d.%m.%Y")
      
      if week == 0:
        v['btn_wprev'].enabled = False
      if year == 0:
        v['btn_yprev'].enabled = False
      
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


# Date Delta Calculation
def delta_between_dates(rule, start_date, end_date):
	delta = rrule.rrule(rule, dtstart=start_date, until=end_date)
	return delta.count()


if __name__ == '__main__':
  w, h = ui.get_screen_size()
  f = (0, 0, w, h)
  view = LifeView(frame=f)
  view.present(style='sheet', hide_title_bar=True)
  
