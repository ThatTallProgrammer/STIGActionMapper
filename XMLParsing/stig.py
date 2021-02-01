class Stig:
    def __init__(self, stig_data: dict) -> None:
        self.vid = stig_data['vid']

    def __str__(self):
        return self.vid
