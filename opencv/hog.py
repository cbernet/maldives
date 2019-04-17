

plt.hist(angle.reshape(-1), weights=norm.reshape(-1), bins=20, range=(0,360))
plt.savefig('hog.png')
plt.show()
