try:
	#for Python2
	from Tkinter import *
except ImportError:
	#for Python3
	from tkinter import *
	
import random

class Application(Frame):

	def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()

		self.location = Location()
		
		self.quit_button = Button(self, text = "Quit", command = self.quit_game)
		self.quit_button.grid(row = 0, column = 99, sticky = E)
		
		self.output_box = Text(self, width = 50, height = 10, wrap = WORD)
		message = " "
		self.output_box.grid(row= 1, columnspan = 100)
		self.display_message(message)
		
		self.button("Start")

	
	def display_message(self, text): #displays  text in the output_box
		self.output_box.delete(0.0, END)
		self.output_box.insert(0.0, text)

	def show_inventory(self): #creates window with inventory

		self.inventory_window = Toplevel()
		self.inventory_window.title("Inventory")
		
		self.output_box_inventory = Text(self.inventory_window, width = 50, height = 10, wrap = WORD)
		self.output_box_inventory.pack()
		text = "Examing your belongings you see that you have: (nothing for now)"
		self.output_box_inventory.insert(0.0, text)

	def show_statistics(self): #creates window with stats

		self.statistics_window = Toplevel()
		self.statistics_window.title("Statistics")
		
		self.output_box_statistics = Text(self.statistics_window, width = 50, height = 10, wrap = WORD)
		self.output_box_statistics.pack()
		
		#hero description

		hero_description_strength = { "weak" : "You are weak.",
									  "medium" : "You are moderately strong.",
									  "powerful" : "You are very strong.",
									  "beast" : "You are freakishly strong."}
		
		hero_description_agility = 	{ "weak" : "You are clumsy.",
									  "medium" : "You are moderately agile.",
									  "powerful" : "You are very agile.",
									  "beast" : "You have fluid, catlike moves."}
		
		hero_description_arcana = 	{ "weak" : "You have no mysterious powers.",
									  "medium" : "You can impact reality with your mind.",
									  "powerful" : "You can bend reality with a mere thought.",
									  "beast" : "You are omnipotent."}

		hero_attribute = []
		hero_attribute_description = []

		for item in [self.my_hero.hero_strenght, self.my_hero.hero_agitity, self.my_hero.hero_arcana]:
			hero_attribute.append(item)

		i = 0

		for element in [hero_description_strength, hero_description_agility, hero_description_arcana]:
			if hero_attribute[i] <= 20:
				hero_attribute_description.append(element["weak"])

			elif hero_attribute[i] <= 40:
				hero_attribute_description.append(element["medium"])

			elif hero_attribute[i] <= 60:
				hero_attribute_description.append(element["powerful"])

			elif hero_attribute[i] <= 80:
				hero_attribute_description.append(element["beast"])

			i += 1

		hero_attribute_description = " ".join(hero_attribute_description)
		
		text = "You are known as " + self.my_hero.name + ". You are a " + self.my_hero.hero_class + ". " + str(hero_attribute_description)

		self.output_box_statistics.insert(0.0, text)

	def button(self, action): #top left button with multiple purposes defined in the method

		try:
			self.primary_button.destroy()
			self.name_entry.destroy()
		except:
			pass

		self.primary_button = Button(self, text = action)
		self.primary_button.grid(row = 0, sticky = W)

		if action == "Start":
			self.primary_button["command"] = self.start_game

		elif action == "Explore":
			self.primary_button["command"] = self.explore

		elif action == "Go back":
			self.primary_button["command"] = self.main_area_game

	def start_game(self):#displays character creation window
		
		#name of character
		
		self.character_creation_window = Toplevel()
		self.character_creation_window.title("Create your character")
		
		self.name_label = Label(self.character_creation_window, text = "Through the ages you've been called: ", font = "Helvetica 10")
		self.name_label.grid(row = 0, column = 0, columnspan = 3, sticky = W)
		
		self.name_entry = Entry(self.character_creation_window)
		self.name_entry.grid(row = 1, column = 1, pady = 5)
		
		#class of character
		
		self.class_label = Label(self.character_creation_window, text = "The bards have been telling ballads of you actions as: ", font = "Helvetica 10")
		self.class_label.grid(row = 2, column = 0, columnspan = 3, sticky = W)
		
		self.choose_class = StringVar()
		self.choose_class.set(None)
		
		Radiobutton(self.character_creation_window,
			text = "a mighty warrior.",
			variable = self.choose_class,
			value = "Your body was hardened by endless battles. Solving problems by force was how you became famous.",
			command = self.choose_class_message
			).grid(row = 3, column = 1, sticky = W)

		Radiobutton(self.character_creation_window,
			text = "a cunning rogue.",
			variable = self.choose_class,
			value = "Silent. Untraceable. Deadly. Your name only in whispers said, only by the brave.",
			command = self.choose_class_message
			).grid(row = 4, column = 1, sticky = W)
	
		Radiobutton(self.character_creation_window,
			text = "a wise sorcerer.",
			variable = self.choose_class,
			value = "Feared because of your arcane powers, esteemed because of your knowledge.",
			command = self.choose_class_message
			).grid(row = 5, column = 1, sticky = W)
		
		self.output_box_class = Text(self.character_creation_window, width = 40, height = 8, wrap = WORD)
		self.output_box_class.grid(row = 6, sticky = W, columnspan = 3)
		
		accept_button = Button(self.character_creation_window, text = "Accept", command = self.get_name)
		accept_button.grid(column = 1) 

	def choose_class_message(self):#displays description of selected class
		message = self.choose_class.get()

		self.output_box_class.delete(0.0, END)
		self.output_box_class.insert(0.0, message) 

	def get_name(self):#checking if name inserted
		name = self.name_entry.get()
		self.chosen_class = self.choose_class.get()
		self.character_creation_window.destroy()
		if not name:
			self.start_game()
		else:
			self.interlude(name) 

	def interlude(self, name): #creating character
		
		if self.chosen_class.startswith("Your body"):
			self.chosen_class = "warrior"
		elif self.chosen_class.startswith("Silent"):
			self.chosen_class = "rogue"
		elif self.chosen_class.startswith("Feared"):
			self.chosen_class = "sorcerer"

		self.my_hero = Hero(name, self.chosen_class)

		self.inventory_button = Button(self, text = "Inventory", command = self.show_inventory).grid(row = 0, column = 1, sticky = W)
		self.statistics_button = Button(self, text = "Statistics", command = self.show_statistics).grid(row = 0, column = 2, sticky = W)
		
		self.main_area_game() 

	def quit_game(self): #closing application
		exit()

	def main_area_game(self): #The main area message.
		message = "You are at your campside"
		self.display_message(message)
		self.button("Explore")

	def explore(self): #Explore message
		location_description = { "forest" : "You have found a forest. It's very dark and gloomy. You can feel beneath you skin a creeping fear.",
								 "valley" : "Wandering about you came across a distant valley. It is sparsely populated by humans.",
								 "mountains" : "Mountains.",
								 "nothing" : "You've already found all available locations. Please give me money to write more."}

		self.location.explore()
		self.display_message(location_description[self.location.current_location])
		self.directions_control()
		self.button("Go back")

	def directions_control(self):
		self.directions_control_window = Toplevel()
		self.directions_control_window.title("Controls")

		self.north_button = Button(self.directions_control_window, text = "North", command = self.move_north)
		self.south_button = Button(self.directions_control_window, text = "South", command = self.move_south)
		self.west_button = Button(self.directions_control_window, text = "West", command = self.move_west)
		self.east_button = Button(self.directions_control_window, text = "East", command = self.move_east)

		self.north_button.grid(row = 0, column = 1)
		self.south_button.grid(row = 2 , column = 1)
		self.west_button.grid(row = 1, column = 0)
		self.east_button.grid(row = 1, column = 2)

	def move_north(self):
		if self.location.current_coordinates_y > 0:
			self.north_button["state"] = "normal"
			self.location.current_coordinates_y -= 1
		else:
			self.north_button["state"] = "disabled"
		print(self.location.current_coordinates_x, self.location.current_coordinates_y)
		self.update_area_description()

	def move_south(self):
		if self.location.current_coordinates_y < 2:
			self.south_button["state"] = "normal"
			self.location.current_coordinates_y += 1
		else:
			self.south_button["state"] = "disabled"
		print(self.location.current_coordinates_x, self.location.current_coordinates_y)
		self.update_area_description()

	def move_west(self):
		if self.location.current_coordinates_x > 0:
			self.west_button["state"] = "normal"
			self.location.current_coordinates_x -= 1
		else:
			self.west_button["state"] = "disabled"
		print(self.location.current_coordinates_x, self.location.current_coordinates_y)
		self.update_area_description()

	def move_east(self):
		if self.location.current_coordinates_x < 2:
			self.east_button["state"] = "normal"
			self.location.current_coordinates_x += 1
		else:
			self.east_button["state"] = "disabled"
		print(self.location.current_coordinates_x, self.location.current_coordinates_y)
		self.update_area_description()

	def update_area_description(self):

		forest_instance_description = { 1 : "The darkest part of forest.",
										2 : "Miejcie nadzieje",
										3 : "nie te lichą marną",
										4 : "co rdzeń spróchniały",
										5 : "w wątły kwiat ubiera",
										6 : "lecz te niezłomną",
										7 : "która tkwi jak ziarno, przyszłych poświęceń w duszy bohatera",
										8 : "This is an entrance to the forest. There is nothing out of ordinary here",
										9 : "A wild creek runs deep in the ravine"}

		if self.location.current_location == "forest":
			message = forest_instance_description[self.location.forest_grid[self.location.current_coordinates_y][self.location.current_coordinates_x]]
		elif self.location.current_location == "valley":
			message = self.location.valley_grid[self.location.current_coordinates_y][self.location.current_coordinates_x]
		elif self.location.current_location == "mountains":
			message = self.location.mountains_grid[self.location.current_coordinates_y][self.location.current_coordinates_x]
		self.display_message(message)

class Hero(object):
	def __init__(self, name, hero_class):
		self.name = name
		self.hero_class = hero_class
		self.hero_inventory = []
		#hero atributes
		self.hero_strenght = 20
		self.hero_agitity = 20
		self.hero_vitality = 20
		self.hero_arcana = 20

		if self.hero_class == "warrior":
			self.hero_strenght += 10
			self.hero_agitity += 5
			self.hero_vitality += 20
			self.hero_arcana -= 20

		elif self.hero_class == "rogue":
			self.hero_agitity += 30
			self.hero_vitality += 10
			self.hero_arcana -= 20

		elif self.hero_class == "sorcerer":
			self.hero_strenght -= 10
			self.hero_vitality -= 5
			self.hero_arcana += 30

class Location(object):
	def __init__(self):

		self.available_locations = ["forest", "valley", "mountains"]
		
		self.current_coordinates_x = 1
		self.current_coordinates_y = 1

		self.forest_found = False
		self.valley_found = False
		self.mountains_found = False

		self.forest_grid = []
		self.valley_grid = []
		self.mountains_grid = []
		n = 1

		for _ in range(3):
			row = []

			for _ in range(3):
				row.append(n)
				n +=1

			self.forest_grid.append(row)
			self.valley_grid.append(row)
			self.mountains_grid.append(row)

	def explore(self):
		try:
			if self.forest_found:
				self.available_locations.remove("forest")
		except:
			pass

		try:
			if self.valley_found:
				self.available_locations.remove("valley")
		except:
			pass

		try:
			if self.mountains_found:
				self.available_locations.remove("mountains")
		except:
			pass
					
		print(self.available_locations)

		if not self.available_locations:
			self.current_location = "nothing"
		else:
			i = random.randrange(len(self.available_locations))

			if self.available_locations[i] == "forest":
				self.forest()

			elif self.available_locations[i] == "valley":
				self.valley()

			elif self.available_locations[i] == "mountains":
				self.mountains()

	def forest(self):
		print("forest\n")
		for row in self.forest_grid:
			print(row)
		self.current_location = "forest"
		self.current_coordinates_x = 1
		self.current_coordinates_y = 2
		
		self.forest_found = True

	def valley(self):
		print("valley\n")
		for row in self.valley_grid:
			print(row)
		self.current_location = "valley"
		self.current_coordinates_x = 1
		self.current_coordinates_y = 1
		self.valley_found = True

	def mountains(self):
		print("mountains\n")
		for row in self.mountains_grid:
			print(row)
		self.current_location = "mountains"
		self.current_coordinates_x = 1
		self.current_coordinates_y = 1
		self.mountains_found = True

if __name__ == "__main__":
	root = Tk()
	root.title("Graphical User Interface Test")
	app = Application(root)
	app.pack()
	root.mainloop()
