import tkinter as tk
from typing import List, Tuple, Optional

Point = Tuple[float, float]


class PointsEditor(tk.Frame):
    def __init__(self, master=None, initial_points: Optional[List[Point]] = None, title: str = "Pontos", **kwargs):
        super().__init__(master, **kwargs)

        tk.Label(self, text=title, font=("Helvetica", 12)).pack(pady=(10, 5))

        entry_row = tk.Frame(self)
        entry_row.pack(fill=tk.X, pady=2)

        tk.Label(entry_row, text="X:", font=("Helvetica", 11)).grid(row=0, column=0, padx=(0, 5))
        self.entry_x = tk.Entry(entry_row, width=10, font=("Helvetica", 11))
        self.entry_x.grid(row=0, column=1)

        tk.Label(entry_row, text="Y:", font=("Helvetica", 11)).grid(row=0, column=2, padx=(10, 5))
        self.entry_y = tk.Entry(entry_row, width=10, font=("Helvetica", 11))
        self.entry_y.grid(row=0, column=3)

        btns_row = tk.Frame(self)
        btns_row.pack(fill=tk.X, pady=4)

        self.btn_add = tk.Button(btns_row, text="Adicionar", font=("Helvetica", 11), command=self._add_point)
        self.btn_add.pack(side=tk.LEFT)

        self.btn_update = tk.Button(btns_row, text="Atualizar", font=("Helvetica", 11), command=self._update_selected)
        self.btn_update.pack(side=tk.LEFT, padx=5)

        self.btn_remove = tk.Button(btns_row, text="Remover", font=("Helvetica", 11), command=self._remove_selected)
        self.btn_remove.pack(side=tk.LEFT)

        self.btn_clear = tk.Button(btns_row, text="Limpar", font=("Helvetica", 11), command=self._clear)
        self.btn_clear.pack(side=tk.LEFT, padx=5)

        list_frame = tk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(4, 0))

        self.listbox = tk.Listbox(list_frame, height=8, font=("Helvetica", 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.listbox.bind("<Double-1>", self._load_selected_into_entries)

        self._points: List[Point] = []

        if initial_points:
            self.set_points(initial_points)

    def get_points(self) -> List[Point]:
        return list(self._points)

    def set_points(self, pts: List[Point]):
        self._points = list(pts)
        self._refresh_listbox()

    def _parse_entries(self) -> Optional[Point]:
        try:
            x = float(self.entry_x.get())
            y = float(self.entry_y.get())
            return (x, y)
        except ValueError:
            return None

    def _add_point(self):
        pt = self._parse_entries()
        if pt is None:
            return  
        self._points.append(pt)
        self._refresh_listbox(select_last=True)

    def _update_selected(self):
        sel = self._get_selected_index()
        if sel is None:
            return
        pt = self._parse_entries()
        if pt is None:
            return
        self._points[sel] = pt
        self._refresh_listbox(select_index=sel)

    def _remove_selected(self):
        sel = self._get_selected_index()
        if sel is None:
            return
        del self._points[sel]
        self._refresh_listbox()

    def _clear(self):
        self._points.clear()
        self._refresh_listbox()

    def _get_selected_index(self) -> Optional[int]:
        sel = self.listbox.curselection()
        if not sel:
            return None
        return sel[0]

    def _load_selected_into_entries(self, event=None):
        sel = self._get_selected_index()
        if sel is None:
            return
        x, y = self._points[sel]
        self.entry_x.delete(0, tk.END)
        self.entry_x.insert(0, str(x))
        self.entry_y.delete(0, tk.END)
        self.entry_y.insert(0, str(y))

    def _refresh_listbox(self, select_last: bool = False, select_index: int | None = None):
        self.listbox.delete(0, tk.END)
        for x, y in self._points:
            self.listbox.insert(tk.END, f"({x:.3f}, {y:.3f})")
        if select_last and self._points:
            idx = len(self._points) - 1
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(idx)
            self.listbox.see(idx)
        elif select_index is not None and 0 <= select_index < len(self._points):
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(select_index)
            self.listbox.see(select_index)
