# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 20:26:31 2020

@author: kieup
"""
SPACE = " "
NUM_SPACE = 4
LIST_STD = ['typing']
file_path = "./data/igviz.py"
file1 = open(file_path, 'r') 

Lines = file1.readlines() 


class Element():
    def __init__(self, this_parent=None, this_name=None):
        self.data = {}
        self.Parent = this_parent
        self.Use= set()
        self.isUsed = set()
        self.name = this_name
        self.real_name = this_name
        
    def __str__(self):
        return self.real_name
    
    def add_data(self, this_name, this_value):
        self.data[this_name] = this_value


class Parser():
    def __init__(self, namespace_curr='main'):
        self.level_curr = 0
        self.level_prev = 0
        self.element_curr= None
        self.element_prev= None
        self.space_curr = 0
        self.space_prev = 0
        self.comment = False
        self.current_call = False
        self.count_space = 0
        self.data = {}
        
        self.namespace_curr = namespace_curr
        self.namespace_prev = [x for x in namespace_curr]
        
        self.second_pass=False
        
    def parse_import(self, this_line):
        as_str = ' as '
        import_str = 'import '
        start_import_ind = this_line.find(import_str) + len(import_str)
        if this_line.find(as_str) >= 0:
            import_name = this_line[(this_line.find(as_str) + len(as_str)):].strip()
            real_name = this_line[start_import_ind : this_line.find(as_str)]
            
            if import_name not in self.data:
                self.data[import_name] = Element(this_name=import_name)
                self.data[import_name].real_name = real_name
        else:
            tmp = this_line[start_import_ind:]
            if tmp == '*':
                # import all
                return None
            else:
                for this_func in tmp.split(','):
                    this_name = this_func.strip()
                    if this_name not in self.data:
                        self.data[this_name] = Element(this_name=this_name)
                    
                    
        return None
    def parse_def_class(self, this_line):
        # called when beginning with def or class
        start_index = this_line.find(' ') + 1
        end_index = this_line.find('(')
        this_name = this_line[start_index:end_index]
        #tmp_name = self.namespace_curr + '.' + this_name
        if not self.second_pass:
            if this_name not in self.data:
                self.data[this_name] = Element(this_parent = self.namespace_curr,
                                               this_name = this_name)
            else:
                this_name_namespace = self.namespace_curr + '.' + this_name
                self.data[this_name_namespace] = Element(this_parent = self.namespace_curr,
                                               this_name = this_name_namespace)
                
        self.element_prev = self.element_curr
        self.element_curr = self.data[this_name]
        return None
    
    def parse_line(self, this_line):
        self.count_space = 0
        if this_line.strip() == '':
            return None
        if len(this_line) == 0:
            return None
        
        for i in range(len(this_line)):
            this_char = this_line[i]
            if this_char  == SPACE:
                self.count_space += 1
            elif this_char  == '#':
                # this line is a comment
                return None
            elif this_char  == '"' and self.count_space == NUM_SPACE: 
                self.comment = not self.comment
                return None
            else:
                # TODO: i is the start of the command
                tmp = this_line[i:]
                break
        if self.comment:
            return None
        else:
            if not self.current_call:
                if self.space_curr != self.count_space:
                    tmp_level = int(self.count_space / NUM_SPACE)
                    self.level_prev = self.level_curr
                    self.level_curr = tmp_level
                    
                    self.space_prev = self.space_curr
                    self.space_curr = self.count_space
            
            if tmp[-1] == ',':
                self.current_call = True
            else:
                self.current_call=False
            
            if tmp[:3] == 'def' or tmp[:5] == 'class':
                self.parse_def_class(tmp)
            elif tmp[:6] == 'import' or tmp[:4] == 'from':
                self.parse_import(tmp)
            
            if self.second_pass:
                for this_element in self.data:
                    if this_element in tmp and this_element != self.element_curr.name:
                        self.element_curr.Use.add(self.data[this_element].name)
                        self.data[this_element].isUsed.add(self.element_curr.name)
                
            return tmp


if __name__ == '__main__':
    this_parser = Parser(namespace_curr='igviz')
    for this_index in range(len(Lines)):
        _ = this_parser.parse_line(Lines[this_index])
    print()
    this_parser.second_pass = True
    
    for this_index in range(len(Lines)):
        _ = this_parser.parse_line(Lines[this_index])
    
    # print(this_parser.data['plot'].Use)
    for this_element in this_parser.data:
        print(this_parser.data[this_element].name)
        print("Is used in: ", this_parser.data[this_element].isUsed)
        print("Use ", this_parser.data[this_element].Use )
        print()
        
        
def test():
    this_line = Lines[7]
    count = 0
    for i in range(len(this_line)):
        
        if i == SPACE:
            count += 1
        else:
            break
    print(i, count)
#test()
        
        
    