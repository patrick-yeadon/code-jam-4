from tkinter import *
from tkinter.ttk import *
from project.contact import Contact


class Controller(Tk):
    """
    Controller Class:

    === Public Attributes ===
    frames: Dictionary of all available pages

    === Methods ===
    show_frame: Allows the switching from one page to another.
                Each page is like a layer in a photo editor,
                calling 'frame.tkraise()' essentially brings
                the specified frame to the top layer, where
                it can be interacted with.
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry('250x300')
        for i in range(5):
            self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)
        notebook = Notebook(self)
        notebook.grid(row=0, column=0, columnspan=5, rowspan=5, sticky=N+S+E+W)

        for page in [ContactsPage, AddContactPage, SettingsPage]:
            page = Frame(notebook)
            notebook.add(page, text='Tab')


class ContactsPage(Frame):
    """
    Contacts Page:
        Contains the list of currently added contacts

    === Public Attributes ===
    master: The frame containing all information on this page
    controller: Reference to the Controller Class

    contacts_list: Dictionary of contacts, each contact is a Contact class instance,
                    each key is the name of the contact

    scroll_bar: Scroll bar that controls what is viewable in the contacts list;
                won't scroll if nothing is in the list, or everything is already
                shown.
    contacts_field: Area where contacts are shown; 10 at a time

    show_info: Button that updates the info_field with the information of the
                currently selected contact
    info_field: Listbox that contains the information of the currently selected contact
    info_scroll: Scrollbar that controls what is viewable in the info_field; won't
                    scroll if nothing is in the list, or everything is already shown

    contacts: Button that takes the user to the 'Contacts' page
    new_contact: Button that takes the user to the 'Add New Contact' page
    settings: Button that takes the user to the 'Settings' page

    === Methods ===
    create: Initializes objects & places them on the page
    insert_contact: Adds a contact's name to the end of the contacts field
    show_contact_info: Shows the information of the selected contact in the info listbox
    """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        # Initialize object names
        self.contacts_list = {}

        self.scroll_bar = None
        self.contacts_field = None
        self.show_info = None
        self.info_field = None
        self.info_scroll = None

        self.contacts = None
        self.new_contact = None
        self.settings = None

        # Create objects
        self.create()

    def create(self):
        self.info_scroll = Scrollbar(self, orient=VERTICAL)
        self.info_field = Listbox(
            self,
            yscrollcommand=self.info_scroll.set
        )
        self.info_scroll.config(command=self.info_field.yview)
        self.info_field.grid(row=3, column=0, columnspan=3, sticky=N+S+E+W)
        self.info_scroll.grid(row=3, column=3, sticky=N+S+E+W)

        self.show_info = Button(self, text="Show Info", command=lambda: self.show_contact_info())
        self.show_info.grid(row=2, column=0, columnspan=3, sticky=N+S+E+W)

        self.contacts = Button(self, text="Contacts", command=lambda: self.controller.show_frame(ContactsPage))
        self.contacts.grid(row=0, column=0, sticky=N+S+E+W)

        self.new_contact = Button(self, text="New Contact", command=lambda: self.controller.show_frame(AddContactPage))
        self.new_contact.grid(row=0, column=1, sticky=N+S+E+W)

        self.settings = Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        self.settings.grid(row=0, column=2, sticky=N+S+E+W)

        self.scroll_bar = Scrollbar(self)
        self.scroll_bar.grid(row=1, column=3, sticky=N+S+E+W)

        self.contacts_field = Listbox(
            self,
            yscrollcommand=self.scroll_bar.set
        )
        self.contacts_field.grid(row=1, column=0, columnspan=3, sticky=N+S+E+W)

        self.scroll_bar.config(command=self.contacts_field.yview)

        for i in range(3):
            self.grid_rowconfigure(i, weight=1)

        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def insert_contact(self, contact):
        self.contacts_field.insert(END, contact)

    def show_contact_info(self):
        name = self.contacts_field.curselection()
        print('DEBUG', name)


class AddContactPage(Frame):
    """
    Add New Contact Page:

    === Public Attributes ===
    master: The frame containing all information on this page
    controller: Reference to the Controller Class

    contact_new: Contact class instance that holds the data that the
                user inputs; when the user submits, the information is
                stored on the contacts_list in ContactsPage.

    Each contact has 5 attributes:
    - Name
    - Phone Number
    - Email
    - Address
    - Notes
    Each attribute has the corresponding objects on the page:
    - A Label
    - A Text Entry Box
    - A Button to add the information to the preview, & update the contact
    The only exception being the Phone Number, which requires the user to
        choose whether the phone number is for Home, Work, or Personal.
        This is done using a Radiobutton, which can only have one value
        chosen at a time. The value of the Radiobutton is tied to a
        StringVar called phone_type_var. When the user clicks 'Add' next
        to the phone number, the StringVar is passed into the
        add_phone_number method.

    clear: Button that clears all text entries
    add_to_contacts: Button that adds the current contact to the contact_list
                    on ContactsPage
    text_entries: List of all text entries; can be looped over to perform a
                    repetitive task on each entry. e.g Clearing all entries

    preview_scroll: Scrollbar that control what is viewable in the preview
                    Listbox
    preview: Listbox that shows the info of the contact being created currently

    contacts: Button that takes the user to the 'Contacts' page
    new_contact: Button that takes the user to the 'Add New Contact' page
    settings: Button that takes the user to the 'Settings' page

    === Methods ===
    create: Initializes objects & places them on the page
    add_contact: Adds contact to the contact_list in ContactsPage;
                If the contact is new, the name of the contact is added to
                the contacts Listbox on ContactsPage.
    clear_all: Loops over all text entries and clears them
    """
    def __init__(self, master, controller, **kw):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        # Initialize object names
        self.contact_new = Contact('')

        self.enter_name = None
        self.enter_name_label = None
        self.enter_name_button = None

        # PLACEHOLDER FOR ACTUAL PHONE NUMBER ENTRY
        self.enter_phone_num = None
        self.phone_type_home = None
        self.phone_type_work = None
        self.phone_type_personal = None
        self.enter_phone_num_label = None
        self.enter_phone_num_button = None
        self.phone_type_var = None

        self.enter_email = None
        self.enter_email_label = None
        self.enter_email_button = None

        self.enter_address = None
        self.enter_address_label = None
        self.enter_address_button = None

        self.enter_notes = None
        self.enter_notes_label = None
        self.enter_notes_button = None

        self.clear = None
        self.add_to_contacts = None

        self.preview_scroll = None
        self.preview = None

        self.contacts = None
        self.new_contact = None
        self.settings = None

        self.text_entries = [self.enter_name, self.enter_phone_num, self.enter_email, self.enter_address,
                             self.enter_notes]

        # Create objects
        self.create()

    def create(self):
        self.preview_scroll = Scrollbar(self, orient=VERTICAL)
        self.preview = Listbox(
            self,
            yscrollcommand=self.preview_scroll.set
        )
        self.preview_scroll.config(command=self.preview.yview)
        self.preview.grid(row=8, column=0, columnspan=3, sticky=N+S+E+W)
        self.preview_scroll.grid(row=8, column=4, sticky=N+S+E+W)

        self.add_to_contacts = Button(self, text="Submit to Contacts", command=lambda: self.add_contact())
        self.add_to_contacts.grid(row=7, column=0, columnspan=2, sticky=N+S+E+W)

        self.clear = Button(self, text="Clear All", command=lambda: self.clear_all())
        self.clear.grid(row=7, column=2, sticky=N+S+E+W)

        self.enter_notes = Entry(self)
        self.enter_notes_label = Label(self, text="Notes:")
        self.enter_notes_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_note(self.enter_notes.get())
        )
        self.enter_notes_button.grid(row=6, column=4, sticky=N+S+E+W)
        self.enter_notes_label.grid(row=6, column=0, sticky=N+S+E+W)
        self.enter_notes.grid(row=6, column=1, columnspan=3, sticky=N+S+E+W)

        self.enter_address = Entry(self)
        self.enter_address_label = Label(self, text="Address")
        self.enter_address_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_address("Physical", self.enter_address.get())
        )
        self.enter_address_label.grid(row=5, column=0, sticky=N+S+E+W)
        self.enter_address.grid(row=5, column=1, columnspan=3, sticky=N+S+E+W)
        self.enter_address_button.grid(row=5, column=4, sticky=N+S+E+W)

        self.enter_email = Entry(self)
        self.enter_email_label = Label(self, text="Email:")
        self.enter_email_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_address("Email", self.enter_email.get())
        )
        self.enter_email_label.grid(row=4, column=0, sticky=N+S+E+W)
        self.enter_email.grid(row=4, column=1, columnspan=3, sticky=N+S+E+W)
        self.enter_email_button.grid(row=4, column=4, sticky=N+S+E+W)

        # PLACEHOLDER FOR ACTUAL PHONE NUMBER ENTRY
        self.enter_phone_num = Entry(self)
        self.enter_phone_num_label = Label(self, text="Phone:")
        phone_type_var = StringVar()
        self.phone_type_home = Radiobutton(self, text="Home", variable=phone_type_var, value="Home")
        self.phone_type_work = Radiobutton(self, text="Work", variable=phone_type_var, value="Work")
        self.phone_type_personal = Radiobutton(self, text="Personal", variable=phone_type_var, value="Personal")
        self.enter_phone_num_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.add_phone_number(self.phone_type_var, self.enter_phone_num.get())
        )
        self.enter_phone_num_label.grid(row=2, column=0, sticky=N+S+E+W)
        self.enter_phone_num.grid(row=2, column=1, columnspan=3, sticky=N+S+E+W)
        self.phone_type_home.grid(row=3, column=0, sticky=N+S+E+W)
        self.phone_type_work.grid(row=3, column=1, sticky=N+S+E+W)
        self.phone_type_personal.grid(row=3, column=2, sticky=N+S+E+W)
        self.enter_phone_num_button.grid(row=2, column=4, sticky=N+S+E+W)

        self.enter_name = Entry(self)
        self.enter_name_label = Label(self, text="Name:")
        self.enter_name_button = Button(
            self,
            text="Add",
            command=lambda: self.contact_new.change_name(self.enter_name.get())
        )
        self.enter_name_button.grid(row=1, column=4, sticky=N+S+E+W)
        self.enter_name_label.grid(row=1, column=0, sticky=N+S+E+W)
        self.enter_name.grid(row=1, column=1, columnspan=3, sticky=N+S+E+W)

        self.contacts = Button(self, text="Contacts", command=lambda: self.controller.show_frame(ContactsPage))
        self.contacts.grid(row=0, column=0, sticky=N+S+E+W)

        self.new_contact = Button(self, text="New Contact", command=lambda: self.controller.show_frame(AddContactPage))
        self.new_contact.grid(row=0, column=1, sticky=N+S+E+W)

        self.settings = Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        self.settings.grid(row=0, column=2, sticky=N+S+E+W)

        for i in range(8):
            self.grid_rowconfigure(i, weight=1)

        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

    def add_contact(self):
        name = self.contact_new.name
        if name == '':
            if name not in self.controller.frames[ContactsPage].contacts_list:
                print("DEBUG: Creating new contact")
                self.controller.frames[ContactsPage].contacts_list[name] = self.new_contact
                self.controller.frames[ContactsPage].insert_contact(name)
            elif name in self.controller.frames[ContactsPage].contacts_list:
                print("DEBUG: Updating already existing contact")
                self.controller.frames[ContactsPage].contacts_list[name] = self.new_contact
        else:
            print("DEBUG: Entered empty name")

    def clear_all(self):
        for entry in self.text_entries:
            print("DEBUG: Deleting", entry)
            entry.delete(0, END)


class SettingsPage(Frame):
    """
        Settings Page:

        === Public Attributes ===
        master: The frame containing all information on this page
        controller: Reference to the Controller Class

        contacts: Button that takes the user to the 'Contacts' page
        new_contact: Button that takes the user to the 'Add New Contact' page
        settings: Button that takes the user to the 'Settings' page

        === Methods ===
        create: Initializes objects & places them on the page
        """
    def __init__(self, master, controller):
        Frame.__init__(self, master)
        self.master = master
        self.controller = controller

        # Initialize object names
        self.contacts = None
        self.new_contact = None
        self.settings = None

        # Create objects
        self.create()

    def create(self):
        self.contacts = Button(self, text="Contacts", command=lambda: self.controller.show_frame(ContactsPage))
        self.contacts.grid(row=0, column=0, sticky=N+S+E+W)

        self.new_contact = Button(self, text="New Contact", command=lambda: self.controller.show_frame(AddContactPage))
        self.new_contact.grid(row=0, column=1, sticky=N+S+E+W)

        self.settings = Button(self, text="Settings", command=lambda: self.controller.show_frame(SettingsPage))
        self.settings.grid(row=0, column=2, sticky=N+S+E+W)


if __name__ == "__main__":
    app = Controller()
    app.mainloop()
