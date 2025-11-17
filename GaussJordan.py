import numpy as np

class GaussJordan:
    def __init__(self, A):
        self.A = A.astype(float).copy()
        self.m, self.n = self.A.shape

    def compute_rref_with_highlight(self):
        row = 0
        steps = []

        # -------- FORWARD ELIMINATION --------
        for col in range(self.n):
            if row >= self.m:
                break  # no more rows

            # Find a pivot in this column
            pivot_row = None
            for r in range(row, self.m):
                if self.A[r, col] != 0:
                    pivot_row = r
                    break
            if pivot_row is None:
                continue  # no pivot in this column

            # Swap pivot row into place
            if pivot_row != row:
                prev = self.A.copy()
                self.A[[row, pivot_row]] = self.A[[pivot_row, row]]
                curr = self.A.copy()
                instr = f"Bytt rad {row+1} med rad {pivot_row+1} for å få ikke-null pivot."
                steps.append({
                    "prev": prev, "curr": curr,
                    "instr": instr, "highlight": row
                })

            # Normalize pivot row to make pivot = 1
            pivot = self.A[row, col]
            if pivot != 1:
                prev = self.A.copy()
                self.A[row] /= pivot
                curr = self.A.copy()
                instr = f"Divider rad {row+1} med {pivot:.2f} for å gjøre pivot til 1."
                steps.append({
                    "prev": prev, "curr": curr,
                    "instr": instr, "highlight": row
                })

            # Eliminate values below pivot
            for r in range(row + 1, self.m):
                val = self.A[r, col]
                if val != 0:
                    prev = self.A.copy()
                    self.A[r] -= val * self.A[row]
                    curr = self.A.copy()
                    instr = (
                        f"Trekk {val:.2f} * rad {row+1} fra rad {r+1} for "
                        f"å gjøre kolonne {col+1} null under pivot."
                    )
                    steps.append({
                        "prev": prev, "curr": curr,
                        "instr": instr, "highlight": r
                    })

            row += 1  # move to next row

        # -------- BACKWARD ELIMINATION --------
        for r in reversed(range(self.m)):
            # Find pivot column for this row (if any)
            pivot_col = None
            for c in range(self.n):
                if self.A[r, c] == 1:
                    pivot_col = c
                    break

            if pivot_col is None:
                continue  # skip zero rows

            # Eliminate above pivot
            for upper_r in range(r):
                val = self.A[upper_r, pivot_col]
                if val != 0:
                    prev = self.A.copy()
                    self.A[upper_r] -= val * self.A[r]
                    curr = self.A.copy()
                    instr = (
                        f"Trekk {val:.2f} * rad {r+1} fra rad {upper_r+1} "
                        f"for å gjøre kolonne {pivot_col+1} null over pivot."
                    )
                    steps.append({
                        "prev": prev, "curr": curr,
                        "instr": instr, "highlight": upper_r
                    })

        return self.A, steps
