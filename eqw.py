import numpy as np
import matplotlib.pyplot as plt

# Load data
data = np.loadtxt('observed_spectrum1.txt')
wavelength = data[:, 0]
flux = data[:, 1]
print('min wavelength=', min(wavelength), 'max wavelength= ', max(wavelength))
plt.plot(wavelength, flux)
plt.show()


# Ask for user input for initial plotting
central_wavelength = float(input("Enter central wavelength (e.g., 5168.42): "))
width = float(input("Enter wavelength width (e.g., 1): "))

# Define plotting range
lower_bound = central_wavelength - width / 2
upper_bound = central_wavelength + width / 2

# Mask and plot selected region
mask = (wavelength >= lower_bound) & (wavelength <= upper_bound)
wavelength_selected = wavelength[mask]
flux_selected = flux[mask]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(wavelength_selected, flux_selected, label='Flux')
ax.set_xlabel('Wavelength (Å)')
ax.set_ylabel('Flux')
ax.set_title(f'Click to select EW range near {central_wavelength} Å')
ax.grid(True)
ax.legend()
points = []

# Interactive selection
def onclick(event):
    if event.inaxes != ax:
        return
    points.append(event.xdata)
    ax.axvline(x=event.xdata, color='red', linestyle='--')
    plt.draw()
    if len(points) == 2:
        plt.close()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
plt.show()

# Ensure two points were selected
if len(points) < 2:
    print("You must click two points to define the wavelength range.")
else:
    initial, final = sorted(points)
    mask_ew = (wavelength >= initial) & (wavelength <= final)
    wavelength_ew = wavelength[mask_ew]
    flux_ew = flux[mask_ew]

    delta_lambda = np.mean(np.diff(wavelength_ew))
    equivalent_width = np.sum((1 - flux_ew) * delta_lambda)*1000
    print(f"Equivalent Width between {initial:.2f} Å and {final:.2f} Å: {equivalent_width:.4f} mÅ")

    # Plot the final selected region
    plt.figure(figsize=(8, 5))
    plt.plot(wavelength_ew, flux_ew, label='Selected Region for EW')
    plt.xlabel('Wavelength (Å)')
    plt.ylabel('Flux')
    plt.title(f'Final EW Range: {initial:.2f}–{final:.2f} Å')
    plt.axhline(1.0, color='gray', linestyle='--', linewidth=0.8)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

