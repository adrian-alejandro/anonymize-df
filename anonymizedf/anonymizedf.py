import random
from faker import Faker


class Anonymize(object):
    """Initializes a Pandas DataFrame as an anonymize object
    to be used for making fake data.

    Args:
        df: takes a Pandas DataFrame

    Returns:
        anonymize object
    """

    def __init__(self, df, locale="en_GB"):

        if df.__class__.__name__ != "DataFrame":
            raise Exception(f"{df} is not a pandas DataFrame.")

        self._df = df
        self._fake = Faker(locale)

    def fake_names(self, original_name, gender_col=None, genders=None, chaining=False):

        """Generates as many fake names as there are unique
        names in the original_name column.

        Args:
            original_name: name column for generating fake names
            chaining: set to true if you want to do method chaining
            gender_col: gender column so to generate gender-specific fake names
            genders: list of genders, first element should correspond to the dataset's equivalent of 'male'

        Returns:
            Pandas DataFrame if chaining is false (default)
            or anonymize object if chaining is true
        """

        # you might be wondering why this if statement (and others like it) are here
        # it's because this is required as a "None" value by interface tools
        # one example being the Alteryx interface designer
        if not original_name:
            print("No name column selected")
            return self
        else:

            if gender_col is not None:

                grouped_names = (
                    self._df.groupby(gender_col)[original_name]
                    .agg(['unique'])
                    .reset_index()
                )

                # just for dev purpose now to check if it ran
                print(f"Grouped by {gender_col}")

                name_dict = {}

                for i, gender in enumerate(grouped_names[gender_col]):
                    gender_name_dict = {
                        name: self._fake.name_male()
                        if gender == genders[0] else self._fake.name_female()
                        for name in grouped_names['unique'][i]
                    }
                    name_dict.update(gender_name_dict)
            else:

                unique_names = self._df[original_name].unique()

                name_dict = {name: self._fake.name() for name in unique_names}

            self._df[f"Fake_{original_name}"] = [
                name_dict[name] for name in self._df[original_name]
            ]
            if chaining:
                return self
            else:
                return self._df

    def fake_ids(self, original_id, chaining=False):

        """Generates as many fake ids as there are unique
        ids in the original_id column.

        Args:
            original_id: id column for generating fake ids
            chaining: set to true if you want to do method chaining

        Returns:
            Pandas DataFrame if chaining is false (default)
            or anonymize object if chaining is true
        """

        if not original_id:
            print("No id column selected")
            return self
        else:

            unique_ids = self._df[original_id].unique()

            id_dict = {id_: self._fake.bban() for id_ in unique_ids}

            self._df[f"Fake_{original_id}"] = [
                id_dict[id_] for id_ in self._df[original_id]
            ]

            if chaining:
                return self
            else:
                return self._df

    def fake_whole_numbers(self, original_whole_number, group_by=None, chaining=False):

        """Takes the min and max of the original_whole_number column
        and generates as many whole numbers in that range as are in
        the original_whole_number column

        Args:
            original_whole_number: number column for generating fake numbers
            chaining: set to true if you want to do method chaining
            group_by: column on which to group_by

        Returns:
            Pandas DataFrame if chaining is false (default)
            or anonymize object if chaining is true
        """

        if not original_whole_number:
            print("No whole number column selected")
            return self
        else:

            if group_by is not None:
                dff = self._df[[group_by, original_whole_number]]

                grouped_numbers = (
                    self._df.groupby(group_by)[original_whole_number]
                    .agg([min, max])
                    .reset_index()
                )

                # just for dev purpose now to check if it ran
                print(f"Grouped by {group_by}")

                whole_number_dict = {}

                for i in range(len(grouped_numbers[group_by])):
                    whole_number_dict_part = {
                        number: self._fake.random_int(
                            min=grouped_numbers["min"][i], max=grouped_numbers["max"][i]
                        )
                        for number in dff[
                            dff[group_by] == grouped_numbers[group_by][i]
                        ][original_whole_number]
                    }
                    whole_number_dict.update(whole_number_dict_part)
            else:
                whole_numbers = self._df[original_whole_number]

                whole_number_dict = {
                    number: self._fake.random_int(
                        min=min(whole_numbers), max=max(whole_numbers)
                    )
                    for number in whole_numbers
                }

            self._df[f"Fake_{original_whole_number}"] = [
                whole_number_dict[number] for number in self._df[original_whole_number]
            ]

            if chaining:
                return self
            else:
                return self._df

    def fake_decimal_numbers(
        self, original_decimal_number, group_by=None, chaining=False
    ):

        """Takes the min and max of the original_decimal_number column
        and generates as many decimal numbers in that range as are in
        the original_decimal_number column

        Args:
            original_decimal_number: number column for generating fake numbers
            chaining: set to true if you want to do method chaining
            group_by: column on which to group_by

        Returns:
            Pandas DataFrame if chaining is false (default)
            or anonymize object if chaining is true
        """

        if not original_decimal_number:
            print("No decimal number column selected")
            return self
        else:

            if group_by is not None:
                dff = self._df[[group_by, original_decimal_number]]

                grouped_numbers = (
                    self._df.groupby(group_by)[original_decimal_number]
                    .agg([min, max])
                    .reset_index()
                )

                # just for dev purpose now to check if it ran
                print(f"Grouped by {group_by}")

                decimal_number_dict = {}

                for i in range(len(grouped_numbers[group_by])):
                    decimal_number_dict_part = {
                        number: round(
                            random.uniform(
                                grouped_numbers["min"][i], grouped_numbers["max"][i]
                            ),
                            2,
                        )
                        for number in dff[
                            dff[group_by] == grouped_numbers[group_by][i]
                        ][original_decimal_number]
                    }
                    decimal_number_dict.update(decimal_number_dict_part)
            else:
                decimal_numbers = self._df[original_decimal_number]

                decimal_number_dict = {
                    number: round(
                        random.uniform(min(decimal_numbers), max(decimal_numbers)), 2
                    )
                    for number in decimal_numbers
                }

            self._df[f"Fake_{original_decimal_number}"] = [
                decimal_number_dict[number]
                for number in self._df[original_decimal_number]
            ]

            if chaining:
                return self
            else:
                return self._df

    def fake_dates(self, original_date, chaining=False):

        """Generates as many dates as there are in the original_date column.
        Currently, doesn't sample the min or max date range but rather
        generates a date string between January 1, 1970 and now.

        Args:
            original_date: date column for generating fake dates
            chaining: set to true if you want to do method chaining

        Returns:
            Pandas DataFrame if chaining is false (default)
            or anonymize object if chaining is true
        """

        if not original_date:
            print("No date column selected")
            return self
        else:

            dates = self._df[original_date]

            date_dict = {date: self._fake.date() for date in dates}

            self._df[f"Fake_{original_date}"] = [
                date_dict[date] for date in self._df[original_date]
            ]

            if chaining:
                return self
            else:
                return self._df

    def fake_categories(self, original_category, chaining=False):

        """Generates as many fake categories as there are unique
        categories in the original_category column.

        Currently, takes the name of the category column and increments it
        ex. segment 1, segment 2 if there are two unique values
        in a category column called segment.

        Args:
            original_category: category column for generating fake categories
            chaining: set to true if you want to do method chaining

        Returns:
            Pandas DataFrame if chaining is false (default)
            or anonymize object if chaining is true
        """

        if not original_category:
            print("No category column selected")
            return self
        else:

            categories = self._df[original_category]

            unique_categories = self._df[original_category].unique()

            category_dict = {
                category: categories.name + " " + str(iteration)
                for iteration, category in enumerate(unique_categories, start=1)
            }

            self._df[f"Fake_{original_category}"] = [
                category_dict[category] for category in self._df[original_category]
            ]

            if chaining:
                return self
            else:
                return self._df

    def show_data_frame(self):
        """Used to return a Pandas DataFrame as the last
        step in a method chain.

        Args:
            this method has no arguments
            - it has good relationships with everyone :)

        Returns:
            Pandas DataFrame
        """
        return self._df
