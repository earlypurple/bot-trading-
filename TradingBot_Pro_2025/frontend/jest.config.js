module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src/tests'],
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'node'],
  setupFilesAfterEnv: [],
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
};
