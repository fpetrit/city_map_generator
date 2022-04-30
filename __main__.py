import pkg.config as conf
from pkg.display.Window import Window

win = Window((750, 400), conf.APP_THEME_COLOR)

win.mainloop()