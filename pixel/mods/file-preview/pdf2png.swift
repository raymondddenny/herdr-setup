// Renders each page of a PDF ($1) to a PNG in $2 at 2x with macOS PDFKit,
// printing "<file> <width> <height>" per page. Built once by build.sh.
import AppKit
import PDFKit

let args = CommandLine.arguments
guard args.count == 3, let doc = PDFDocument(url: URL(fileURLWithPath: args[1])), !doc.isLocked else { exit(1) }
// ponytail: first 300 pages only; page-on-demand rendering if huge PDFs matter.
for i in 0..<min(doc.pageCount, 300) {
    guard let page = doc.page(at: i) else { continue }
    let box = page.bounds(for: .mediaBox)
    let image = page.thumbnail(of: NSSize(width: box.width * 2, height: box.height * 2), for: .mediaBox)
    guard let tiff = image.tiffRepresentation, let rep = NSBitmapImageRep(data: tiff),
          let png = rep.representation(using: .png, properties: [:]) else { continue }
    let name = "page-\(i + 1).png"
    try png.write(to: URL(fileURLWithPath: args[2]).appendingPathComponent(name))
    print(name, rep.pixelsWide, rep.pixelsHigh)
}
