module.exports = function (api) {
  api.cache(true);
  return {
    presets: ["babel-preset-expo"],
    plugins: [
      [
        "module-resolver",
        {
          root: ["."],
          extensions: [".jsx", ".js", ".json"],
          alias: {
            assets: "./assets",
            theme: "./src/theme",
            services: "./src/services",
            features: "./src/features",
            navigation: "./src/navigation",
          },
        },
      ],
    ],
  };
};
