from pyopengltk import OpenGLFrame
from OpenGL.GL import *
from typing import List, Tuple

Point = Tuple[float, float]


class OpenGLCanvas(OpenGLFrame):
    def __init__(self, *args, width=800, height=600, **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)
        self.width = width
        self.height = height
        self.bind("<Configure>", self._on_configure)
        self.pontos: List[Point] = []
        self._viewport_center: Tuple[float, float] = (0.0, 0.0)
        self._viewport_half_extent: float = 1.0
        self._viewport_initialized: bool = False

    def _compute_view_params(self) -> Tuple[float, float, float]:
        """Retorna centro (cx, cy) e meio alcance para enquadrar os pontos."""
        if not self.pontos:
            return 0.0, 0.0, 1.0

        xs = [x for x, _ in self.pontos]
        ys = [y for _, y in self.pontos]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        cx = (min_x + max_x) / 2.0
        cy = (min_y + max_y) / 2.0

        half_width = max(max_x - min_x, 0.1) / 2.0
        half_height = max(max_y - min_y, 0.1) / 2.0
        half_extent = max(half_width, half_height, 0.5)

        return cx, cy, half_extent * 1.05

    def _update_view_params(self) -> None:
        cx, cy, half_extent = self._compute_view_params()
        self._viewport_center = (cx, cy)
        self._viewport_half_extent = max(half_extent, 1e-3)
        self._viewport_initialized = True

    def _ensure_view_params(self, auto_center: bool) -> None:
        if auto_center or not self._viewport_initialized:
            self._update_view_params()
        elif self.pontos:
            xs = [x for x, _ in self.pontos]
            ys = [y for _, y in self.pontos]
            half_width = max(max(xs) - min(xs), 0.1) / 2.0
            half_height = max(max(ys) - min(ys), 0.1) / 2.0
            half_extent = max(half_width, half_height, 0.5) * 1.05
            if half_extent > self._viewport_half_extent:
                self._viewport_half_extent = half_extent

    def _apply_projection(self) -> None:
        cx, cy = self._viewport_center
        half_extent = self._viewport_half_extent
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        aspect = self.width / self.height if self.height else 1.0
        if aspect >= 1.0:
            half_extent_x = half_extent * aspect
            half_extent_y = half_extent
        else:
            half_extent_x = half_extent
            half_extent_y = half_extent / max(aspect, 1e-6)

        glOrtho(cx - half_extent_x, cx + half_extent_x, cy - half_extent_y, cy + half_extent_y, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def _on_configure(self, evt):
        self.width, self.height = evt.width, evt.height
        try:
            glViewport(0, 0, self.width, self.height)
            self.after(0, self._display)
        except Exception:
            pass

    def initgl(self):
        print("[OpenGLCanvas] initgl: size=", self.width, self.height)
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glViewport(0, 0, self.width, self.height)

        self.pontos = [(-0.5, -0.5), (0.5, -0.5), (0.5, 0.5), (-0.5, 0.5)]
        self._update_view_params()
        try:
            self.after(0, self._display)
        except Exception:
            pass

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)

        self._apply_projection()

        glLineWidth(1.0)
        glPointSize(1.0)

        cx, cy = self._viewport_center
        half_extent = self._viewport_half_extent
        aspect = self.width / self.height if self.height else 1.0
        if aspect >= 1.0:
            half_extent_x = half_extent * aspect
            half_extent_y = half_extent
        else:
            half_extent_x = half_extent
            half_extent_y = half_extent / max(aspect, 1e-6)
        left = cx - half_extent_x
        right = cx + half_extent_x
        bottom = cy - half_extent_y
        top = cy + half_extent_y

        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_LINES)
        if bottom <= 0 <= top:
            glVertex2f(left, 0.0)
            glVertex2f(right, 0.0)
        if left <= 0 <= right:
            glVertex2f(0.0, bottom)
            glVertex2f(0.0, top)
        glEnd()

        glColor3f(0.0, 0.0, 0.0)
        if self.pontos:
            modo = GL_LINE_LOOP if len(self.pontos) > 2 else GL_LINE_STRIP
            glBegin(modo)
            for x, y in self.pontos:
                glVertex2f(x, y)
            glEnd()

    def set_pontos(self, pontos: List[Point], auto_center: bool = True):
        self.pontos = pontos
        self._ensure_view_params(auto_center)
        try:
            self._display()
        except Exception:
            self.after(0, self._display)

    def get_pontos(self) -> List[Point]:
        return list(self.pontos)
