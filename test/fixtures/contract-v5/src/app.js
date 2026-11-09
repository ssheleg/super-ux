export function cancelSubscription(plan) {
  return { ...plan, status: "cancelled" };
}
