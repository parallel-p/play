from PIL import Image, ImageDraw

FRAME_WIDTH = 500
FRAME_HEIGHT = 1000
BORDER = 10
MARGIN = 10


class Painter:
    _is_initialized = False

    def _initialize(self, jury_state):
        self._is_initialized = True
        self._delta_x = ((FRAME_WIDTH - 2 * BORDER) /
                         max(jury_state.heap_sizes))
        self._width = self._delta_x - MARGIN
        self._delta_y = ((FRAME_HEIGHT - 2 * BORDER) /
                         len(jury_state.heap_sizes))
        self._height = self._delta_y - MARGIN

    def paint(self, jury_state):
        '''Paints the state of the game;
        returns the string --- bits of the jpeg image.'''

        if not self._is_initialized:
            self._initialize(jury_state)

        image = Image.new('RGB', (FRAME_WIDTH, FRAME_HEIGHT), (255, 255, 255))
        y = BORDER
        for heap_size in jury_state.heap_sizes:
            x = BORDER
            for i in range(heap_size):
                draw = ImageDraw.Draw(image)
                draw.rectangle(
                    (x, y, x + self._width, y + self._height),
                    fill='gray', outline='black'
                )
                del draw
                x += self._delta_x
            y += self._delta_y
        return str(image.tostring("gif", "RGB"))
