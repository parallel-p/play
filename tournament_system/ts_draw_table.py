class TSDrawTable:
    def _count_width(self, data):
        '''
        Returns width of one column in the table (by simply finding
        maximum width of all cells)
        '''
        width = 0
        for row in data:
            for cell in row:
                width = max(width, len(cell))
        return width

    def _print_separator(self, width, columns):
        '''
        Returns the line of separators '-'.
        Gets width of one column and quantity of columns.
        '''
        return str('+' + '-' * width) * columns + '+'

    def _align(self, cell, width):
        '''
        Aligns data in one cell.
        '''
        format_string = '{:^' + str(width) + '}'
        return format_string.format(cell)

    def draw_table(self, data):
        '''
        Returns list of strings of the table
        '''
        table = []
        #Width of one column
        width = self._count_width(data)
        #Quantity of columns
        columns = len(data) + 1
        table.append(self._print_separator(width, columns))
        for row in data:
            current_string = ''
            for cell in row:
                current_string += '|'
                current_string += self._align(cell, width)
            current_string += '|'
            table.append(current_string)
            table.append(self._print_separator(width, columns))
        return table
