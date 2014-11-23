__author__ = 'jmeline'

from common import JsonConfigHandler as jch

class ConfigManager():
    def __init__(self):
        self.jsonConfig = jch.JsonConfigHandler()
        self.wallhaven_generator = self._page_generator()


    def _page_generator(self):
        pages = self.jsonConfig.extractedObject['wallhaven'].Wallhaven['Page']
        for i in pages:
            yield i

    def wallhaven_URL(self):
        """ Create URL
        :return:
        http://alpha.wallhaven.cc/search?categories=111&purity=100&resolutions=1920x1080&ratios=16x9&sorting=favorites&order=desc

        ** Categories **
        1) General (100)        2) Anime   (010)        3) People  (001)

        ** Purity **
        1) SFW     (100)        2) Sketchy (010)

        ** Resolutions **
        1024x768, 1280x800, 1366x768, 1280x960, 1440x900, 1600x900, 1280x1024, 1600x1200, 1680x1050, 1920x1080,
        1920x1200, 2560x1440, 2560x1600, 3840x1080, 5760x1080, 3840x2160

        ** Ratio **
        4x3, 5x4, 16x9, 16x10, 32x9, 48x9

        ** Sorting **
        Relevance, Random, Date Added, Views, Favorites

        ** Order **
        desc, asc

        """

        try:
            wallhaven = self.jsonConfig.extractedObject['wallhaven'].Wallhaven
            url = "http://alpha.wallhaven.cc/search?categories={category}&purity={purity}&resolutions={resolutions}&sorting={sorting}&order={order}&page={page}".format(
                category=wallhaven['Categories'], purity=wallhaven['Purity'], resolutions=wallhaven['Resolution'], sorting=wallhaven['Sorting'], order=wallhaven['Order'],
                page=next(self.wallhaven_generator)
            )
            return url
        except StopIteration:
            return None
