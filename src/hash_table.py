import numpy as np
# ###############################################


class HashTable:
    def __init__(self, codes: np.ndarray):
        """ Pre-computed hash-table for every code couples
            Contains 3 N by N matrices (where N is the number of codes)

            - M_wp:   the well-placed count matrix
            - M_ip:   the ill-placed count matrix
            - M_h:    the hash matrix (that is a combination of wp & ip)
        """
        code_length = codes.shape[1]
        # list unique symbols from codes
        symbols = np.unique(codes)
        # count how many times each symboles occures in each code
        symbol_occurences = np.hstack([
            (codes == symbol).sum(axis=1, keepdims=True) 
            for symbol in symbols])
        # generate upper triangular matrix (without diagonal) indices
        Y, X = np.triu_indices(len(codes), 1)
        ## well-placed count matrix
        self.M_wp = np.diag([code_length] * len(codes))
        wp = (codes[Y] == codes[X]).sum(axis=1)
        self.M_wp[Y, X] = wp
        self.M_wp[X, Y] = wp
        ## ill-placed count matrix
        self.M_ip = np.zeros((len(codes), len(codes)))
        ip   = np.minimum(
                symbol_occurences[Y], 
                symbol_occurences[X]
            ).sum(axis=1) - wp
        self.M_ip[Y, X] = ip
        self.M_ip[X, Y] = ip
        ## hash matrix (combination of M_wp & M_ip)
        self.M_h = self.M_wp * code_length + self.M_ip
    # ###############################################
