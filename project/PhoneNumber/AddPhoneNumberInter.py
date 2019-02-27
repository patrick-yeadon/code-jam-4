import tkinter as tk
from project.PhoneNumber.PhoneCanvas import PhoneCanvas, PhoneButton


class AddPhoneNumberInter(tk.Frame):
    #TODO document AddPhoneNumberInter class

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.text_label = tk.Label(self, font=('Calibri', 10), fg='#63FF20', bg='#00536a', borderwidth=2,
                                   text="Please enter the phone number you which\n to add with the rotary phone below.")
        self.label_frame = tk.Frame(self, bg='#00536a')
        self.phone_number_label = PhoneNumberEntry(self.label_frame, font=('Calibri', 20), fg='#63FF20', bg='#00536a', width=12,
                                                   borderwidth=2, relief='sunken')

        self.button = tk.Button(self.label_frame, text='Clear', bg='#00536a', font=('Calibri', 14), height=1,
                                command=self.phone_number_label.clear_phone_number)

        self.text_label.pack(side=tk.TOP)
        self.phone_number_label.pack(side=tk.LEFT, )
        self.button.pack(side=tk.LEFT)
        self.label_frame.pack(side=tk.TOP)

        self.phone_canvas = PhoneCanvas(self)
        self.phone_canvas.pack(side=tk.TOP)
        self.pack()

        self.master.bind("<<Send_Phone_Number>>", self.__get_phone_number)

    def __get_phone_number(self, event):
        number = self.phone_canvas.send_output_number()
        if number is not None:
            self.add_phone_number_to_entry(number)

    def add_phone_number_to_entry(self, num: int):
        self.phone_number_label.add_phone_number(num)


class PhoneNumberEntry(tk.Label):
    #TODO document PhoneNumberEntry class

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

    def add_phone_number(self, num: int):
        current_text = self['text']
        current_length = len(current_text)
        if current_length == 12:
            return
        if current_length == 3 or current_length == 7:
            self['text'] = self['text'] + '-'
        self['text'] = self['text'] + num

    def clear_phone_number(self):
        self['text'] = ''

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("300x375")
    root.resizable(False, False)
    AddPhoneNumberInter(root, bg='#00536a')
    root.mainloop()
