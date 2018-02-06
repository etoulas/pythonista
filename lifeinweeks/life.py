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


scroll = ui.ScrollView()
scroll.width = w
scroll.height = h
scroll.background_color = 'white'
scroll.content_size = (w, NUM_YEARS * SIZE + 100)
scroll.always_bounce_vertical = True
scroll.always_bounce_horizontal = True


def button_action(week, year):
  def button_tapped(sender):
    v = ui.load_view('lifeweek')
    txt = 'week {}, year {}'.format(week, year)
    v['lbl_weekyear'].text = txt
    v['btn_wprev'].action = button_action(week-1, year)
    v['btn_wnext'].action = None
    v['btn_yprev'].action = None
    v['btn_ynext'].action = None
    nv = sender.navigation_view
    #nv.pop_view()
    nv.push_view(v)
    
    def home_tapped(sender):
      #nv = sender.navigation_view
      #nv['lifeweek'].close()
    btni_home = ui.ButtonItem(title='Home')
    btni_home.action = home_tapped
    nv.right_button_items = [btni_home]
  return button_tapped


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
    scroll.add_subview(button)


v = ui.NavigationView(scroll)
v.name = 'Life Calendar'
v.present('sheet')
