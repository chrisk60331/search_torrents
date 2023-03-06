class Torrent:
    """Class to represent torrent metadata."""

    def __init__(
        self,
        title: str,
        link: str,
        size: str = "",
        seed: int = 0,
        leech: int = 0,
    ):
        self.title = title
        self.link = link
        self.size = size
        self.seed = seed
        self.leech = leech

    def __str__(self):
        return (
            "\n"
            f"title: {self.title}\n"
            f"size: {self.size}\n"
            f"link: {self.link}\n"
            f"seed: {self.seed}\n"
            f"leech: {self.leech}\n"
            "\n"
        )

    def __repr__(self):
        return (
            f"Torrent(title={self.title}, "
            f"size={self.size}, link={self.link}, "
            f"seed={self.seed}, leach={self.leech})\n"
        )
