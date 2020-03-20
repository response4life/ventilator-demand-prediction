import model
if __name__ == "__main__":
    # execute only if run as a script
    inputs = model.calculate(950715, run_plot=True)
    model.plot(**inputs)