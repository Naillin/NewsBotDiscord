import string

class NewsUnit:
    def __init__(self, author: str, title: str, description: str, url: str, urlToImage: str):
        """
        Initializes a NewsUnit object with the provided news article information.

        Args:
            author (str): The author of the news article.
            title (str): The title of the news article.
            description (str): A brief description of the news article.
            url (str): The URL of the news article.
            urlToImage (str): The URL of an image associated with the news article.

        Returns:
            None
        """
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.urlToImage = urlToImage

    def __str__(self):
        """
        Returns a string representation of the NewsUnit object.

        Returns:
            str: The title of the news article.
        """
        return self.title