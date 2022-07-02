import numpy as np

def preprocessing_anomaly(X_train, y_train, X_test, y_test, alpha, normal_class):
    '''
    Transform the dataset in a new one for anomaly detection according to Beggel's paper
    alpha: parameter to control the proportion of normal - anomalies
    normal_class: indicate label of the normal class
    '''

    X_total = np.concatenate((X_train, X_test), axis=0)
    y_total = np.concatenate((y_train, y_test), axis=0)
    N, M, _ = X_total.shape

    # select the normal class time series
    N_positive_total = len(X_total[y_total == normal_class])
    # take 80% of normal observation to train as in the paper
    size_positive = round(0.8 * N_positive_total)
    random_indices = np.random.choice(N_positive_total, size=size_positive, replace=False)

    X_train_positive = X_total[y_total == normal_class][random_indices]
    y_train_positive = y_total[y_total == normal_class][random_indices]
    X_test_positive = np.delete(X_total[y_total == normal_class], random_indices, axis=0)
    y_test_positive = np.array([1] * len(X_test_positive))

    # size of the negative samples in training set
    size_negative = round(alpha * len(X_train_positive))
    # take few random negative examples
    random_indices = np.random.choice(N - N_positive_total, size=size_negative, replace=False)
    X_train_negative = X_total[y_total != normal_class][random_indices]
    # collapse all the anomalous ts in one class
    y_train_negative = np.array([-1] * len(random_indices))
    X_test_negative= np.delete(X_total[y_total != normal_class], random_indices, axis=0)
    y_test_negative = np.array([-1] * len(X_test_negative))

    X_train_anomaly = np.concatenate((X_train_positive, X_train_negative), axis=0)
    y_train_anomaly = np.concatenate((y_train_positive, y_train_negative), axis=0)

    X_test_anomaly = np.concatenate((X_test_positive, X_test_negative), axis=0)
    y_test_anomaly = np.concatenate((y_test_positive, y_test_negative), axis=0)

    return X_train_anomaly, y_train_anomaly, X_test_anomaly, y_test_anomaly
