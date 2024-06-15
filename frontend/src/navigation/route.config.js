export const routes = {
  screens: {
    Accounts: {
      screens: {
        Settings: "settings",
      },
    },
    Smallcases: {
      initialRouteName: "SmallcaseList",
      screens: {
        SmallcaseList: "smallcases",
        SmallcaseDetail: "smallcases/:id",
      },
    },
  },
};
