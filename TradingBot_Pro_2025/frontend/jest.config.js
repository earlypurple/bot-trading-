module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/src/tests'],
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'node'],
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
  },
  moduleNameMapper: {
    '\\.(css|less)$': '<rootDir>/src/tests/__mocks__/styleMock.js',
  },
};
