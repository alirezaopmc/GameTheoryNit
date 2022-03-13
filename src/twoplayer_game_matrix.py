import numpy as np

class TwoPlayer_GameMatrix:
  """
  Representation of game matrix
  """

  def __init__(self, matrix) -> None:
      """
      Constructor function

      @param matrix: game matrix
      @example: matrix = [
          ['Ali/Reza'], 'Head', 'Tail'],
          ['Head', 1, -1],
          ['Tail', -1, 1]
        ]

      @property data: the given matrix
      @property playerA: the name of the first player
      @property playerB: the name of the second player
      @property nrow: the number of rows (excluding the strategies row)
      @property ncol: the number of columns (excluding the strategies column)
      @property strategiesA: a list of available strategies for the first player
      @property strategiesB: a list of available strategies for the second player
      """
      self.data = np.array(matrix)
      self.playerA = matrix[0][0][0]
      self.playerB = matrix[0][0][1]
      self.nrow = len(matrix)-1
      self.ncol = len(matrix[0])-1
      self.strategiesA = [ s for s in matrix[0][1:] ]
      self.strategiesB = [ s[0] for s in matrix[1:] ]

  def getStrategyIndex(self, strategyName: str, playerName: str):
    """
    Returns the index of a strategy for the specified player
    
    @param strategyName: the strategy label
    @param playerName: the name of the player
    """
    pass

  def getByIndex(self, i: int, j: int):
    """
    Getter for a specific element in the array by the strategy index
    """
    return self.data[i, j]

  def getByStrategy(self, strategyA: str, strategyB: str):
    """
    Returns the payoff value of the specified strategies for both players

    @param strategyA: strategy label of the first player
    @param strategyA: strategy label of the second player
    """
    indexA = self.getStrategyIndex(strategyA, self.playerA)
    indexB = self.getStrategyIndex(strategyB, self.playerB)

    # the reason for +1 is that strategy labels row and column stands in index=0
    return self.getByIndex(indexA+1, indexB+1)

  def deleteColumn(self, col_i: int):
    """
    Deletes a specific strategy column in the matrix (player 2)

    @param col_i: column index
    """
    strategy = self.data[0, col_i]

    self.strategiesB.remove(strategy)
    self.data = np.delete(self.data, col_i, 1)
    self.ncol -= 1

  def deleteRow(self, row_i: int):
    """
    Deletes a specific strategy row in the matrix (player 1)

    @param row_i: row index
    """
    strategy = self.data[row_i, 0]

    self.strategiesA.remove(strategy)
    self.data = np.delete(self.data, row_i, 0)
    self.nrow -= 1

  def simplifyBeatenRowsAndColumns(self):
    """
    Returns the simplified version of the matrix and a flag that indicates to the result of the simplification
    """
    matrix: list = self.data.tolist()

    result = TwoPlayer_GameMatrix(matrix.copy())

    # flag    
    changed = True
    while changed:
      changed = False

      def update_rows():
        for row1 in range(1, result.nrow+1):
          for row2 in range(1, result.nrow+1):
            if row1 == row2: continue
            for col in range(1, result.ncol+1):
              if result.data[row1, col] > result.data[row2, col]:
                break
              elif col == result.ncol:
                result.deleteRow(row1)
                return True
        return False

      def update_columns():
        for col1 in range(1, result.ncol+1):
          for col2 in range(1, result.ncol+1):
            if col1 == col2: continue
            for row in range(1, result.nrow+1):
              if result.data[row, col1] > result.data[row, col2]:
                break
              elif row == result.nrow:
                result.deleteColumn(col1)
                return True
        return False

      changed |= update_rows()
      changed |= update_columns()

    return result

  def saddlePoint(self):
    """
    Returns the value of the saddle points in the game matrix
    """

    rows_min_values = [ min(self.data[row, 1:]) for row in range(1, self.nrow+1) ]
    cols_max_values = [ max(self.data[1:, col]) for col in range(1, self.ncol+1) ]

    rows_max_val = max(rows_min_values)
    cols_min_val = min(cols_max_values)

    saddle_rows = []
    saddle_cols = []

    for row in range(len(rows_min_values)):
      if rows_min_values[row] == rows_max_val:
        saddle_rows.append(row+1)

    for col in range(len(cols_max_values)):
      if cols_max_values[col] == cols_min_val:
        saddle_cols.append(col+1)

    return [
      self.data[srow, scol]
      for srow in saddle_rows
        for scol in saddle_cols
    ], {
      'saddle_rows': saddle_rows,
      'saddle_cols': saddle_cols,
    }
