boards = [
  # frozen King
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "P", " ", " ", " "],
  [" ", " ", " ", " ", "K", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "]
  ],
  # one Knight vs King
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", "n", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "p", " ", " ", " "],
  [" ", " ", " ", " ", " ", "B", " ", " "],
  [" ", " ", " ", " ", "K", " ", " ", " "]
  ],
  # one bishop vs King
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "b", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "p", " ", " ", " "],
  [" ", " ", " ", " ", " ", "N", " ", " "],
  [" ", " ", " ", " ", "K", " ", " ", " "]
  ],
  # King & bishop vs King & bishop (same color)
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "b", " ", " ", " "],
  [" ", "B", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "p", " ", " ", " "],
  [" ", " ", " ", " ", " ", "N", " ", " "],
  [" ", " ", " ", " ", "K", " ", " ", " "]
  ],
  # King & bishop vs King & bishop (opposite color)
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "b", " ", " ", " "],
  [" ", " ", " ", " ", "B", " ", " ", " "],
  [" ", " ", " ", " ", "p", " ", " ", " "],
  [" ", " ", " ", " ", " ", "N", " ", " "],
  [" ", " ", " ", " ", "K", " ", " ", " "]
  ],
  # pawn promotion
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", "P"],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "p", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "K", " ", " ", " "]
  ],
  # this state raise an error when in check & black king check only
  [
  [" ", " ", " ", " ", "K", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", "p"],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "], 
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "P", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "k", " ", " ", " "]
  ],
  # rook castle
  [
  ["r", " ", " ", " ", "k", " ", " ", "r"],
  ["p", " ", " ", " ", " ", " ", " ", "p"],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", "B", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  ["P", " ", " ", " ", " ", " ", " ", "P"],
  ["R", " ", " ", " ", "K", " ", " ", "R"]
  ],
  # pawn eat after check
  [
  [" ", " ", " ", " ", "k", " ", " ", " "],
  [" ", "p", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", "p", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", " ", " ", " "],
  [" ", " ", " ", " ", " ", "p", "P", " "],
  [" ", "P", " ", " ", " ", " ", "P", "P"],
  [" ", " ", " ", " ", " ", "K", " ", "P"]
  ],

]
