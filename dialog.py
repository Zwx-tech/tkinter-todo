import customtkinter as ctk
from typing import Optional, Union, Tuple

class CustomDialog(ctk.CTkInputDialog):

    def __init__(self,
                 text: Optional[str] = "",
                 end_date: Optional[str] = "",
                 hour: Optional[str] = "",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 entry_text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 title: str = "CTkDialog",
                 font: Optional[Union[Tuple[str, int], ctk.CTkFont]] = None,
                 text_value: Optional[str] = ""
        
        ):

        super().__init__(fg_color, text_color, button_fg_color, button_hover_color, button_text_color,
                         entry_fg_color, entry_border_color, entry_text_color, title, font, text)

        self._end_date = end_date
        self._hour = hour
        self._text_value = text_value

    def _create_widgets(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.rowconfigure(0, weight=1)

        self._label = ctk.CTkLabel(master=self,
                                   width=300,
                                   wraplength=300,
                                   fg_color="transparent",
                                   text_color=self._text_color,
                                   text=self._text,
                                   font=self._font)
        self._label.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        # Entry for the main text
        self._entry_label = ctk.CTkLabel(master=self,
                                         text="Task Description:",
                                         fg_color="transparent",
                                         text_color=self._text_color,
                                         font=self._font)
        self._entry_label.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="w")
        self._entry = ctk.CTkEntry(master=self,
                                   width=230,
                                   fg_color=self._entry_fg_color,
                                   border_color=self._entry_border_color,
                                   text_color=self._entry_text_color,
                                   font=self._font)
        self._entry.insert(0, self._text_value)
        self._entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")

        # Entry for the end date
        self._end_date_label = ctk.CTkLabel(master=self,
                                            text="End Date(DD-MM-RRRR):",
                                            fg_color="transparent",
                                            text_color=self._text_color,
                                            font=self._font)
        self._end_date_label.grid(row=3, column=0, padx=20, pady=(0, 10), sticky="w")

        self._end_date_entry = ctk.CTkEntry(master=self,
                                            width=230,
                                            fg_color=self._entry_fg_color,
                                            border_color=self._entry_border_color,
                                            text_color=self._entry_text_color,
                                            font=self._font)
        self._end_date_entry.insert(0, self._end_date)
        self._end_date_entry.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="ew", columnspan=2)
        
        # Entry for the hour
        self._hour_label = ctk.CTkLabel(master=self,
                                        text="Hour(HH:MM):",
                                        fg_color="transparent",
                                        text_color=self._text_color,
                                        font=self._font)
        self._hour_label.grid(row=5, column=0, padx=20, pady=(0, 20), sticky="w", columnspan=2)

        self._hour_entry = ctk.CTkEntry(master=self,
                                        width=230,
                                        fg_color=self._entry_fg_color,
                                        border_color=self._entry_border_color,
                                        text_color=self._entry_text_color,
                                        font=self._font)
        self._hour_entry.insert(0, self._hour)
        self._hour_entry.grid(row=6, column=0, padx=20, pady=(0, 20), sticky="ew", columnspan=2)

        self._ok_button = ctk.CTkButton(master=self,
                                        width=100,
                                        border_width=0,
                                        fg_color=self._button_fg_color,
                                        hover_color=self._button_hover_color,
                                        text_color=self._button_text_color,
                                        text='Ok',
                                        font=self._font,
                                        command=self._ok_event)
        self._ok_button.grid(row=7, column=0, columnspan=1, padx=(20, 10), pady=(0, 20), sticky="ew")

        self._cancel_button = ctk.CTkButton(master=self,
                                            width=100,
                                            border_width=0,
                                            fg_color=self._button_fg_color,
                                            hover_color=self._button_hover_color,
                                            text_color=self._button_text_color,
                                            text='Cancel',
                                            font=self._font,
                                            command=self._cancel_event)
        self._cancel_button.grid(row=7, column=1, columnspan=1, padx=(10, 20), pady=(0, 20), sticky="ew")

        self.after(150, lambda: self._entry.focus())
        self._entry.bind("<Return>", self._ok_event)

    def _ok_event(self, event=None):
        self._user_input = self._entry.get()
        self._end_date_input = self._end_date_entry.get()
        self._hour_input = self._hour_entry.get()
        self.grab_release()
        self.destroy()

    def get_input(self):
        self.master.wait_window(self)
        return self._user_input, self._end_date_input, self._hour_input
