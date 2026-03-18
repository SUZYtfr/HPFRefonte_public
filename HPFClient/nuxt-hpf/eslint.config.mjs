import withNuxt from "./.nuxt/eslint.config.mjs";

export default withNuxt({
  languageOptions: {
    ecmaVersion: "latest",
    sourceType: "module",

    parserOptions: {
      requireConfigFile: false,
    },
  },

  rules: {
    quotes: [
      "error",
      "double",
      {
        avoidEscape: true,
      },
    ],

    semi: ["error", "always"],

    "@typescript-eslint/explicit-function-return-type": [
      "error",
      {
        allowExpressions: true,
      },
    ],
    "@typescript-eslint/ban-ts-comment": ["warn"],

    "lines-between-class-members": [
      "error",
      "always",
      {
        exceptAfterSingleLine: true,
      },
    ],

    camelcase: "off",
    "@typescript-eslint/no-inferrable-types": "off",
    "space-before-function-paren": "off",
    "no-use-before-define": "off",
    curly: "off",
    "object-shorthand": "off",
    "no-useless-escape": "off",
    "import/no-mutable-exports": "off",

    "vue/component-name-in-template-casing": ["warn", "PascalCase", { registeredComponentsOnly: false }],
    "vue/prop-name-casing": ["warn", "camelCase"],
    "vue/custom-event-name-casing": ["warn", "camelCase"],
    "vue/first-attribute-linebreak": [
      "warn",
      {
        singleline: "ignore",
        multiline: "below",
      },
    ],
    "vue/require-default-prop": "off",
    "vue/html-self-closing": [
      "error",
      {
        html: { normal: "never", void: "always" },
        svg: "always",
        math: "always",
      },
    ],

    "vue/multi-word-component-names": [
      "off",
      {
        ignores: [],
      },
    ],
  },
});
