import code

class Annotator:
    def __init__(self, df):
        self.df = df.copy()
        self.filtered_df = None

    def choose_column_to_annotate(self):
        column_correctly_spelled = False
        while not column_correctly_spelled:
            print("""
            Here is your list of columns, please choose
            one to annotate.
            """)
            for col in self.df.columns:
                print(col)

            inspect_data = input("""
            Would you like an interactive shell, to
            inspect your data? [yes/no]
            """)
            if inspect_data == "yes":
                print("The data is stored in self.df")
                self.launch_shell()
            column_to_annotate = input("""
            Which column would you like to annotate?
            """)

            try:
                self.df[column_to_annotate]
                column_correctly_spelled = True
            except KeyError:
                print("""
                looks like the column you specified
                isn't in the dataframe, please try 
                again.
                """)
        return column_to_annotate

    def launch_shell(self):
        print("""To exit the interactive shell, 
        please type CTRL-D
        """)
        code.interact(local=locals())
        
    def confirm_column_to_annotate(self, column_to_annotate):
        confirm_column = None
        while confirm_column != "yes":
            confirm_column = input(f"""
            Just to make sure, you want to 
            annotate {column_to_annotate}? [yes/no]
            """)
            if confirm_column != "yes":
                column_to_annotate = self.choose_column_to_annotate()
        return column_to_annotate

    def filter_columns(self):
        print("""
        We will launch an interactive session now.
        Please store all filtered results in 
        self.filtered_df
        Thank you!""")
        self.launch_shell()

    def pre_annotation_instructions(self):
        print("""
        Great!
        Now let's start annotating our data:
        use '1' to indicate yes
        use '0' to indicate no
        use '-1' to indicate not sure
        
        Notice, we are only annotating data in binary this way.
        '1' means our element has membership to the class.
        '0' means our element does not have membership to the class.
        '-1' means we aren't sure of the row's membership.
        
        If you aren't 100% sure, don't label the data.  
        Saying '-1' is always better.
        """)

    def get_columns_to_use(self):
        print("""Next we'll look at which columns to
        use in helping you label the data.
        """)
        if self.filtered_df:
            for col in self.filtered_df:
                print(col)
        else:
            for col in self.df:
                print(col)
        columns = input("""
        Which column(s) do you to use to label the 
        data? (please separate by commas ',') 
        """)
        return [col.strip()
                for col in columns.split(",")]

    def get_label(self, df, index, columns_to_use):
        print("For the following row")
        for column in columns_to_use:
            print(column, df[column].loc[index])
        return input("""
        What should the label be? 
        1 - yes 
        0 - np 
        -1 - not sure
        shell - launch interactive shell
        exit - exit the labeling process and save the data
        """)

    def _annotate(self, columns_to_use, column_to_annotate):
        if self.filtered_df:
            df = self.filtered_df.copy()
        else:
            df = self.df.copy()
        for index in df.index:
            label = self.get_label(df, index, columns_to_use)
            if label.strip() == "shell":
                self.launch_shell()
                label = self.get_label(df, index, columns_to_use)
                df.loc[index, column_to_annotate] = int(label)
            elif label.strip() == "exit":
                return df
            else:
                df.loc[index, column_to_annotate] = int(label)
            
    def annotate(self):
        print("""
        Welcome to the annotator.
        We are going to annotate your data.
        """)
        column_to_annotate = self.choose_column_to_annotate()
        column_to_annotate = self.confirm_column_to_annotate(column_to_annotate)
        print("Great!")

        column_filtering = input("""
        Would you like to filter by any columns? [yes/no]
        """)
        if column_filtering == "yes":
            self.filter_columns()
        
        self.pre_annotation_instructions()
        columns_to_use = self.get_columns_to_use()
        tmp_df = self._annotate(
            columns_to_use,
            column_to_annotate
        )
        df = self.df.copy()
        df[column_to_annotate].loc[tmp_df.index] = tmp_df[column_to_annotate]
        return df
