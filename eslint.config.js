import js from '@eslint/js';
import tseslint from 'typescript-eslint';

// Hard rule 2: no platform-dependent math in sim-core. ECMAScript lets these
// Math functions differ between engines; Math.sqrt and basic arithmetic are exact.
const bannedMath = [
  'random', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'atan2',
  'sinh', 'cosh', 'tanh', 'asinh', 'acosh', 'atanh',
  'exp', 'expm1', 'log', 'log1p', 'log2', 'log10', 'pow', 'cbrt', 'hypot',
].map((property) => ({
  object: 'Math',
  property,
  message: `Math.${property} is banned in sim-core (hard rule 2). Use a deterministic implementation.`,
}));

export default tseslint.config(
  { ignores: ['**/node_modules/**', '**/dist/**'] },
  js.configs.recommended,
  ...tseslint.configs.strict,
  {
    files: ['packages/sim-core/src/**/*.ts'],
    rules: {
      'no-restricted-properties': [
        'error',
        ...bannedMath,
        { object: 'Date', property: 'now', message: 'Wall-clock time breaks determinism (hard rule 2).' },
        { object: 'performance', property: 'now', message: 'Wall-clock time breaks determinism (hard rule 2).' },
      ],
      'no-restricted-syntax': [
        'error',
        {
          selector: "BinaryExpression[operator='**'], AssignmentExpression[operator='**=']",
          message: 'The ** operator has the same engine-dependent precision as Math.pow (hard rule 2).',
        },
        {
          selector: "NewExpression[callee.name='Date']",
          message: 'Date breaks determinism in sim-core (hard rule 2).',
        },
      ],
    },
  },
);
