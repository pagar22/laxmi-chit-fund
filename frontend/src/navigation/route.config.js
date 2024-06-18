export const routes = {
  screens: {
    Accounts: {
      screens: {
        AdminPanel: "admin",
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
