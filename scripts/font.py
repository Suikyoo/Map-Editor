import pygame 
import core_functs

class Font:
    def __init__(self, path):
        self.spacing = 1
        fontPic = pygame.image.load(path).convert()
        self.fontWidth = fontPic.get_width()
        self.fontHeight = fontPic.get_height()
        self.dictionary = {}
        self.wordDict = {}
        width = 0
        self.charOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';', '%', '#']
        self.charCount = 0
        self.totalCharWidth = 0
        self.wordWidth = []
        for x in range(self.fontWidth):
            color = fontPic.get_at((x, 0))
            if color[0] == 127:
                letterPic = core_functs.cut(fontPic, x - width, 0, width, self.fontHeight)
                letterPic.set_colorkey((0, 0, 0))
                self.dictionary[self.charOrder[self.charCount]] = letterPic.copy()
                self.charCount += 1
                width = 0
            else:
                 width += 1

    def render(self, surf, string, coords):
        xOffset = 0
        for i in string:
            if i != " ":
                surf.blit(self.dictionary[i], (coords[0] + xOffset, coords[1]))
                xOffset += self.dictionary[i].get_width()
            else: xOffset += self.dictionary["A"].get_width()        

    def render_lines(self, surf, y, gap, lst, offset=[0, 0]):
        yOffset = 0
        surfWidth = surf.get_width()
        widthCenter = surfWidth/2
        for word in lst:
           wordWidth = self.dictionary["A"].get_width() * len(word)
           wordWidthCenter = wordWidth/2
           self.render(surf, word, (widthCenter - wordWidthCenter + offset[0], y + offset[1] + yOffset))
           yOffset += self.fontHeight + gap

    def get_string_size(self, string):
        text_size = [0, 0]
        for i in range(2):
            for char in string:
                if char == " ": char = "A"
                text_size[i] += self.dictionary[char].get_size()[i]
        return text_size

    def center_render(self, surf, string, coords):
        text_size = self.get_string_size(string) 
        #text_size = [sum([self.dictionary[char].get_size()[i] if char != " " else char = "A" for char in string]) for i in range(2)]
        self.render(surf, string, [coords[i] - text_size[i]/2 for i in range(2)])

        

            
