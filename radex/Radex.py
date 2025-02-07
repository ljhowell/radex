import pandas as pd

from radex.dfsearch import search_dataframe
from radex.expression import Expression
from radex.preprocessing import clean_dataframe


class Radex:
    """
    Base class for running RADEX searches on a dataframe.

    Example usage:
    from radex import Radex
    radex = Radex()
    radex.read_data('data/synthetic_ultrasound_reports/ex_usreports_validation.csv')
    radex.preprocess_data()
    radex.searches = {'thyroid nodule': 'thyr* NEAR2 nodul*'}
    radex.run_searches()
    radex.save_output('output.csv')
    """

    def __init__(self, data=None):
        self.data = data
        self.preprocessed_data = None
        self.output_data = None
        self.searches = None

        # Define example searches
        self.example_searches = {
            "Thyroid_mention": "thyroid",
            "Normal_thyroid": "normal~2thyroid",
            "Post-op": "*thyroidectomy | lobectomy | surg* | resect* | resection* | incomplete~~2thyroid | partial~~2thyroid | post?op",
            "Nodule_mention": "nodul* | thyroid~~4node | thyroid~~2cyst*",
            "Multinodule": "multi?nodul* | mng | nodules | thyroid~~2cysts | thyroid ~~2 nodes",
            "Altered_echotexture": "thyroiditis | grav?s | heterogen* echotexture | inflamed* ~~2thyroid",
            "Goitre": "goit?r? | mng | enlarge*~~3thyroid",
        }

    def read_data(self, file_path):
        """
        Read data from a csv file.

        Args:
            file_path (str): The path to the csv file.
        """
        # Read data from a csv file
        self.data = pd.read_csv(file_path)

    def preprocess_data(self, columns="report", **kwargs):
        """
        Preprocess the data by cleaning the dataframe.

        Args:
            columns (str or list): The columns to preprocess. Defaults to 'report'.
            **kwargs: Additional keyword arguments.
                drop_duplicates (bool, optional): Whether to drop duplicates. Defaults to True.
                drop_nulls (bool, optional): Whether to drop nulls. Defaults to True.
                drop_negatives (str, optional): How to handle negations. Defaults to 'negex'.
                drop_stopwords (str, optional): How to handle stopwords. Defaults to 'nltk'.
        """

        if self.data is None:
            raise ValueError(
                "Data has not been loaded. Call read_data() first."
            )

        # Clean the dataframe
        drop_duplicates = kwargs.get("drop_duplicates", True)
        drop_nulls = kwargs.get("drop_nulls", True)
        drop_negatives = kwargs.get("drop_negatives", "negex")
        drop_stopwords = kwargs.get("drop_stopwords", "nltk")

        self.preprocessed_data = clean_dataframe(
            self.data,
            columns,
            drop_duplicates=drop_duplicates,  # drop duplicate entries
            drop_nulls=drop_nulls,  # drop empty reports
            drop_negatives=drop_negatives,  # remove negated phrases
            drop_stopwords=drop_stopwords,  # remove stopwords
        )

    def run_searches(self):
        """
        Run example searches on the preprocessed data.

        Returns:
            pd.DataFrame: The output data.
        """
        if self.preprocessed_data is None:
            raise ValueError(
                "Data has not been preprocessed. Call preprocess_data() first."
            )

        if self.searches is None:
            raise ValueError("Define searches or use run_example_searches().")

        # Apply each example search
        print(self.searches)
        for filter_name, expression in self.searches.items():
            expression = Expression().parse_string(expression)
            self.output_data = search_dataframe(
                self.preprocessed_data,
                column="report",
                expression=expression,
                new_column_name=filter_name,
            )

        return self.output_data

    def run_example_searches(self):
        """
        Run example searches on the preprocessed data.

        Returns:
            pd.DataFrame: The output data.
        """

        self.searches = self.example_searches
        self.run_searches()

        return self.output_data

    def save_output(self, file_path):
        """
        Save the output data to a csv file.

        Args:
            file_path (str): The path to the csv file.
        """
        if self.output_data is None:
            raise ValueError("No output data. Run searches first.")

        self.output_data.to_csv(file_path, index=False)
