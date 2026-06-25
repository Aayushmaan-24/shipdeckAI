export type Slide = {
  slide: number;
  title: string;
  content: string;
};

export type Status = "idle" | "generating" | "done" | "error";

export function extractMessages(event: Record<string, unknown>): string[] {
  const messages: string[] = [];
  for (const nodeUpdate of Object.values(event)) {
    if (
      nodeUpdate &&
      typeof nodeUpdate === "object" &&
      "messages" in nodeUpdate &&
      Array.isArray((nodeUpdate as { messages: unknown }).messages)
    ) {
      for (const msg of (nodeUpdate as { messages: string[] }).messages) {
        if (typeof msg === "string") {
          messages.push(msg);
        }
      }
    }
  }
  return messages;
}

export function extractDeckStructure(event: Record<string, unknown>): Slide[] | null {
  for (const nodeUpdate of Object.values(event)) {
    if (
      nodeUpdate &&
      typeof nodeUpdate === "object" &&
      "deck_structure" in nodeUpdate
    ) {
      const deck = (nodeUpdate as { deck_structure: Slide[] }).deck_structure;
      if (Array.isArray(deck) && deck.length > 0) {
        return deck;
      }
    }
  }
  return null;
}
