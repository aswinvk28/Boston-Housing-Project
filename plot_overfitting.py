"""
============================
Underfitting vs. Overfitting
============================

This example demonstrates the problems of underfitting and overfitting and
how we can use linear regression with polynomial features to approximate
nonlinear functions. The plot shows the function that we want to approximate,
which is a part of the cosine function. In addition, the samples from the
real function and the approximations of different models are displayed. The
models have polynomial features of different degrees. We can see that a
linear function (polynomial with degree 1) is not sufficient to fit the
training samples. This is called **underfitting**. A polynomial of degree 4
approximates the true function almost perfectly. However, for higher degrees
the model will **overfit** the training data, i.e. it learns the noise of the
training data.
We evaluate quantitatively **overfitting** / **underfitting** by using
cross-validation. We calculate the mean squared error (MSE) on the validation
set, the higher, the less likely the model generalizes correctly from the
training data.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor

def execute(plt, features, prices):
    
    degrees = [1, 4, 15]
    
    for i in range(len(degrees)):
        ax = plt.subplot(1, len(degrees), i + 1)
        plt.setp(ax, xticks=(), yticks=())

        polynomial_features = PolynomialFeatures(degree=degrees[i],
                                             include_bias=False)
        decision_regression = DecisionTreeRegressor()
        pipeline = Pipeline([("polynomial_features", polynomial_features),
                         ("decision_regression", decision_regression)])
        if degrees[i] == 1:
            X = features[['RM', 'LSTAT', 'PTRATIO']]
        elif degrees[i] == 4:
            X = features[['RM', 'PTRATIO']]
        else:
            X = features[['PTRATIO', 'LSTAT']]
        y = prices
        pipeline.fit(X, y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=degrees[i]*0.05)

        # Evaluate the models using crossvalidation
        scores = cross_val_score(pipeline, X, y,
                                scoring="neg_mean_squared_error", cv=10)

        plt.plot(X_test, pipeline.predict(X_test), label="Model")
        # plt.plot(X_test, true_fun(X_test), label="True function")
        if degrees[i] == 1:
            plt.scatter(X.values[:, 0], y, edgecolor='b', s=20, label="Samples")
            plt.scatter(X.values[:, 1], y, edgecolor='b', s=20, label="Samples")
            plt.scatter(X.values[:, 2], y, edgecolor='b', s=20, label="Samples")
        elif degrees[i] == 4:
            plt.scatter(X.values[:, 0], y, edgecolor='b', s=20, label="Samples")
            plt.scatter(X.values[:, 1], y, edgecolor='b', s=20, label="Samples")
        else:
            plt.scatter(X.values[:, 0], y, edgecolor='b', s=20, label="Samples")
            plt.scatter(X.values[:, 1], y, edgecolor='b', s=20, label="Samples")
        plt.xlabel("features")
        plt.ylabel("prices")
        plt.legend(loc="best")
        plt.title("Degree {}\nMSE = {:.2e}(+/- {:.2e})".format(
            degrees[i], -scores.mean(), scores.std()))
    plt.show()
