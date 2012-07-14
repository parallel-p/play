from PIL import Image, ImageDraw
from jury_state import JuryState

FRAME_SIDE = 1024
BORDER = 10


class Painter:
    _is_initialized = False

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._cell_side = FRAME_SIDE / jury_state.field_side

    def paint(self, jury_state):
        '''
        Paints the state of the game;
        Returns the string --- bits of the jpeg image.
        '''
        image = Image.new('RGB', (FRAME_SIDE, FRAME_SIDE), (255, 255, 255))
        if not self._is_initialized:
            self._initialize(jury_state)

        '''
        Start drawing field
        '''
        for i, row in enumerate(jury_state.field):
            for j, cell in enumerate(row):
                x = i * self._cell_side
                y = j * self._cell_side
                rectangle = (y, x, y + self._cell_side, x + self._cell_side)
                if cell == -2:
                    continue
                draw = ImageDraw.Draw(image)
                if cell == -1:
                    draw.rectangle(rectangle, fill='orange', outline='black')
                elif cell == 0:
                    draw.rectangle(rectangle, outline='black')
                else:
                    draw.rectangle(rectangle, fill='black', outline='black')
                del draw
        '''
        Finish drawing field
        '''
        return str(image.tostring("jpeg", "RGB"))
