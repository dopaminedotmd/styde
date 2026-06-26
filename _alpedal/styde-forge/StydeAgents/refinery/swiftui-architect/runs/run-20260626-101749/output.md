```swift
// StydeApp.swift
import SwiftUI
import SwiftData
@main
struct StydeApp: App {
    let container: ModelContainer
    init() {
        do {
            let config = ModelConfiguration(isStoredInMemoryOnly: false)
            container = try ModelContainer(
                for: Course.self, Challenge.self, Achievement.self, UserProfile.self,
                configurations: config
            )
            let context = container.mainContext
            if try context.fetchCount(FetchDescriptor<UserProfile>()) == 0 {
                StydeSeeder.seed(in: context)
            }
        } catch {
            fatalError("Failed to create ModelContainer: \(error)")
        }
    }
    var body: some Scene {
        WindowGroup {
            ContentView()
                .modelContainer(container)
        }
    }
}
// MARK: - Models
@Model
final class Course {
    @Attribute(.unique) var id: UUID
    var title: String
    var subtitle: String
    var category: String
    var progress: Double
    var totalLessons: Int
    var completedLessons: Int
    var isEnrolled: Bool
    var thumbnailSymbol: String
    var difficulty: String
    init(id: UUID = UUID(), title: String, subtitle: String, category: String, progress: Double = 0, totalLessons: Int = 10, completedLessons: Int = 0, isEnrolled: Bool = false, thumbnailSymbol: String = "book.fill", difficulty: String = "Intermediate") {
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.category = category
        self.progress = progress
        self.totalLessons = totalLessons
        self.completedLessons = completedLessons
        self.isEnrolled = isEnrolled
        self.thumbnailSymbol = thumbnailSymbol
        self.difficulty = difficulty
    }
}
@Model
final class Challenge {
    @Attribute(.unique) var id: UUID
    var title: String
    var description_: String
    var type: String
    var xpReward: Int
    var isCompleted: Bool
    var createdAt: Date
    init(id: UUID = UUID(), title: String, description: String, type: String, xpReward: Int, isCompleted: Bool = false, createdAt: Date = Date()) {
        self.id = id
        self.title = title
        self.description_ = description
        self.type = type
        self.xpReward = xpReward
        self.isCompleted = isCompleted
        self.createdAt = createdAt
    }
}
@Model
final class Achievement {
    @Attribute(.unique) var id: UUID
    var title: String
    var subtitle: String
    var symbol: String
    var isUnlocked: Bool
    var unlockedAt: Date?
    init(id: UUID = UUID(), title: String, subtitle: String, symbol: String, isUnlocked: Bool = false, unlockedAt: Date? = nil) {
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.symbol = symbol
        self.isUnlocked = isUnlocked
        self.unlockedAt = unlockedAt
    }
}
@Model
final class UserProfile {
    @Attribute(.unique) var id: UUID
    var name: String
    var email: String
    var totalXP: Int
    var streakDays: Int
    var avatarSymbol: String
    init(id: UUID = UUID(), name: String = "Learner", email: String = "learner@styde.ai", totalXP: Int = 0, streakDays: Int = 0, avatarSymbol: String = "person.circle.fill") {
        self.id = id
        self.name = name
        self.email = email
        self.totalXP = totalXP
        self.streakDays = streakDays
        self.avatarSymbol = avatarSymbol
    }
}
// MARK: - Seeder
struct StydeSeeder {
    static func seed(in context: ModelContext) {
        let profile = UserProfile(name: "Alex", email: "alex@styde.ai", totalXP: 2840, streakDays: 12, avatarSymbol: "person.circle.fill")
        context.insert(profile)
        let courses: [(String, String, String, Double, String, String)] = [
            ("SwiftUI Mastery", "Build declarative UIs from zero to production", "iOS Development", 0.45, "book.circle.fill", "Advanced"),
            ("Machine Learning Fundamentals", "Neural networks, regression, and classification", "AI/ML", 0.72, "brain.head.profile.fill", "Intermediate"),
            ("AR Quick Start", "Build your first ARKit experience in a weekend", "AR/VR", 0.0, "arkit", "Beginner"),
            ("System Design", "Distributed systems at FAANG scale", "Computer Science", 0.18, "server.rack", "Advanced"),
            ("Data Structures", "Algorithms and problem solving patterns", "Computer Science", 0.91, "flowchart.fill", "Intermediate"),
            ("iOS Animations", "Fluid transitions with SwiftUI and Core Animation", "iOS Development", 0.33, "sparkles.rectangle.stack", "Intermediate"),
        ]
        for (title, subtitle, category, progress, symbol, difficulty) in courses {
            let completed = Int(progress * 24)
            let course = Course(
                title: title, subtitle: subtitle, category: category,
                progress: progress, totalLessons: 24, completedLessons: completed,
                isEnrolled: true, thumbnailSymbol: symbol, difficulty: difficulty
            )
            context.insert(course)
        }
        let challenges: [(String, String, String, Int)] = [
            ("Daily Code Challenge", "Implement a binary search tree in 15 minutes", "coding", 50),
            ("Quiz: Swift Protocols", "Test your knowledge of protocol-oriented programming", "quiz", 30),
            ("Watch & Learn", "Complete one ARKit tutorial video today", "video", 40),
            ("Peer Review", "Review and comment on three community projects", "social", 60),
        ]
        for (title, desc, type, xp) in challenges {
            let challenge = Challenge(title: title, description: desc, type: type, xpReward: xp)
            context.insert(challenge)
        }
        let achievements: [(String, String, String, Bool)] = [
            ("First Steps", "Complete your first course", "figure.walk", true),
            ("Streak Master", "7-day learning streak", "flame.fill", true),
            ("Knowledge Seeker", "Complete 50 lessons", "books.vertical.fill", true),
            ("Challenge Ace", "Complete 10 daily challenges", "trophy.fill", false),
            ("Course Collector", "Enroll in 10 courses", "square.stack.3d.up.fill", true),
            ("Night Owl", "Study after midnight for 3 days", "moon.stars.fill", false),
        ]
        for (title, subtitle, symbol, unlocked) in achievements {
            let ach = Achievement(title: title, subtitle: subtitle, symbol: symbol, isUnlocked: unlocked, unlockedAt: unlocked ? Date().addingTimeInterval(-Double.random(in: 86400...604800)) : nil)
            context.insert(ach)
        }
        try? context.save()
    }
}
// MARK: - Combine Services
import Combine
final class StydeService {
    static let shared = StydeService()
    let progressUpdatePublisher = PassthroughSubject<UUID, Never>()
    let challengeCompletePublisher = PassthroughSubject<UUID, Never>()
    let xpUpdatePublisher = CurrentValueSubject<Int, Never>(0)
    func updateProgress(courseId: UUID, newProgress: Double) {
        progressUpdatePublisher.send(courseId)
    }
    func completeChallenge(challengeId: UUID, xpReward: Int) {
        challengeCompletePublisher.send(challengeId)
        xpUpdatePublisher.value += xpReward
    }
}
// MARK: - ViewModels
@MainActor
final class DashboardViewModel: ObservableObject {
    @Published var activeCourses: [Course] = []
    @Published var todayChallenges: [Challenge] = []
    @Published var dailyXP: Int = 0
    @Published var streakDays: Int = 0
    @Published var isLoading = false
    private var cancellables = Set<AnyCancellable>()
    private var modelContext: ModelContext?
    func setup(with context: ModelContext) {
        self.modelContext = context
        loadData()
        StydeService.shared.progressUpdatePublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in self?.loadData() }
            .store(in: &cancellables)
        StydeService.shared.xpUpdatePublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] xp in self?.dailyXP = xp }
            .store(in: &cancellables)
    }
    func loadData() {
        guard let context = modelContext else { return }
        isLoading = true
        let courseDescriptor = FetchDescriptor<Course>(predicate: #Predicate { $0.isEnrolled && $0.progress < 1.0 }, sortBy: [SortDescriptor(\.progress, order: .reverse)])
        activeCourses = (try? context.fetch(courseDescriptor)) ?? []
        let challengeDescriptor = FetchDescriptor<Challenge>(predicate: #Predicate { !$0.isCompleted })
        todayChallenges = (try? context.fetch(challengeDescriptor)) ?? []
        let profileDescriptor = FetchDescriptor<UserProfile>()
        if let profile = try? context.fetch(profileDescriptor).first {
            streakDays = profile.streakDays
        }
        isLoading = false
    }
    func completeChallenge(_ challenge: Challenge) {
        guard let context = modelContext else { return }
        challenge.isCompleted = true
        challenge.createdAt = Date()
        StydeService.shared.completeChallenge(challengeId: challenge.id, xpReward: challenge.xpReward)
        let profileDescriptor = FetchDescriptor<UserProfile>()
        if let profile = try? context.fetch(profileDescriptor).first {
            profile.totalXP += challenge.xpReward
        }
        try? context.save()
        loadData()
    }
}
@MainActor
final class ExploreViewModel: ObservableObject {
    @Published var courses: [Course] = []
    @Published var searchQuery = ""
    @Published var selectedCategory: String? = nil
    @Published var recommendedCourses: [Course] = []
    @Published var trendingTopics: [(String, Int)] = []
    var categories: [String] {
        Array(Set(courses.map(\.category))).sorted()
    }
    var filteredCourses: [Course] {
        var result = courses
        if !searchQuery.isEmpty {
            result = result.filter { $0.title.localizedCaseInsensitiveContains(searchQuery) || $0.subtitle.localizedCaseInsensitiveContains(searchQuery) }
        }
        if let category = selectedCategory {
            result = result.filter { $0.category == category }
        }
        return result
    }
    private var modelContext: ModelContext?
    func setup(with context: ModelContext) {
        self.modelContext = context
        loadData()
    }
    func loadData() {
        guard let context = modelContext else { return }
        let descriptor = FetchDescriptor<Course>(sortBy: [SortDescriptor(\.title)])
        courses = (try? context.fetch(descriptor)) ?? []
        recommendedCourses = courses.filter { !$0.isEnrolled }.shuffled()
        let categoryCounts = Dictionary(grouping: courses, by: \.category).mapValues { $0.count }
        trendingTopics = categoryCounts.sorted { $0.value > $1.value }.map { ($0.key, $0.value) }
    }
    func enrollCourse(_ course: Course) {
        guard let context = modelContext else { return }
        course.isEnrolled = true
        try? context.save()
        loadData()
    }
}
@MainActor
final class ProfileViewModel: ObservableObject {
    @Published var profile: UserProfile?
    @Published var achievements: [Achievement] = []
    @Published var totalCourses: Int = 0
    @Published var completedCourses: Int = 0
    @Published var totalChallenges: Int = 0
    @Published var completedChallenges: Int = 0
    private var modelContext: ModelContext?
    private var cancellables = Set<AnyCancellable>()
    func setup(with context: ModelContext) {
        self.modelContext = context
        loadData()
        StydeService.shared.xpUpdatePublisher
            .receive(on: DispatchQueue.main)
            .sink { [weak self] _ in self?.loadData() }
            .store(in: &cancellables)
    }
    func loadData() {
        guard let context = modelContext else { return }
        let profileDescriptor = FetchDescriptor<UserProfile>()
        profile = try? context.fetch(profileDescriptor).first
        let achievementDescriptor = FetchDescriptor<Achievement>(sortBy: [SortDescriptor(\.isUnlocked, order: .reverse)])
        achievements = (try? context.fetch(achievementDescriptor)) ?? []
        let courseDescriptor = FetchDescriptor<Course>(predicate: #Predicate { $0.isEnrolled })
        let enrolled = (try? context.fetch(courseDescriptor)) ?? []
        totalCourses = enrolled.count
        completedCourses = enrolled.filter { $0.progress >= 1.0 }.count
        let challengeDescriptor = FetchDescriptor<Challenge>()
        let allChallenges = (try? context.fetch(challengeDescriptor)) ?? []
        totalChallenges = allChallenges.count
        completedChallenges = allChallenges.filter(\.isCompleted).count
    }
}
// MARK: - Views
struct ContentView: View {
    @State private var selectedTab = 0
    @Environment(\.modelContext) private var modelContext
    @StateObject private var dashboardVM = DashboardViewModel()
    @StateObject private var exploreVM = ExploreViewModel()
    @StateObject private var profileVM = ProfileViewModel()
    var body: some View {
        TabView(selection: $selectedTab) {
            DashboardView(vm: dashboardVM)
                .tabItem {
                    Label("Dashboard", systemImage: selectedTab == 0 ? "house.fill" : "house")
                }
                .tag(0)
            ExploreView(vm: exploreVM)
                .tabItem {
                    Label("Explore", systemImage: selectedTab == 1 ? "magnifyingglass.circle.fill" : "magnifyingglass.circle")
                }
                .tag(1)
            ProfileView(vm: profileVM)
                .tabItem {
                    Label("Profile", systemImage: selectedTab == 2 ? "person.fill" : "person")
                }
                .tag(2)
        }
        .tint(.indigo)
        .onAppear {
            dashboardVM.setup(with: modelContext)
            exploreVM.setup(with: modelContext)
            profileVM.setup(with: modelContext)
        }
    }
}
struct DashboardView: View {
    @ObservedObject var vm: DashboardViewModel
    @Environment(\.modelContext) private var modelContext
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    headerSection
                    weeklyStreakSection
                    activeCoursesSection
                    dailyChallengesSection
                }
                .padding()
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("Dashboard")
            .refreshable { vm.loadData() }
        }
    }
    private var headerSection: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text("Welcome back, \(vm.streakDays > 0 ? "Streak Master 🔥" : "Learner")")
                .font(.title2).fontWeight(.bold)
            Text("Keep your momentum going!")
                .font(.subheadline).foregroundColor(.secondary)
            HStack {
                Label("\(vm.dailyXP) XP today", systemImage: "bolt.fill")
                    .font(.caption).foregroundColor(.indigo)
                Spacer()
                Label("\(vm.todayChallenges.count) challenges", systemImage: "flag.fill")
                    .font(.caption).foregroundColor(.orange)
            }
            .padding(.top, 4)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .shadow(color: .black.opacity(0.05), radius: 4, x: 0, y: 2)
    }
    private var weeklyStreakSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Label("Weekly Streak", systemImage: "flame.fill")
                .font(.headline).foregroundColor(.orange)
            HStack(spacing: 8) {
                ForEach(0..<7) { day in
                    let isActive = day < vm.streakDays % 7
                    VStack(spacing: 4) {
                        Circle()
                            .fill(isActive ? Color.orange : Color(.systemGray5))
                            .frame(width: 32, height: 32)
                            .overlay(Text(["M","T","W","T","F","S","S"][day]).font(.caption2).fontWeight(isActive ? .bold : .regular).foregroundColor(isActive ? .white : .secondary))
                    }
                }
            }
        }
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .shadow(color: .black.opacity(0.05), radius: 4, x: 0, y: 2)
    }
    private var activeCoursesSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Active Courses").font(.headline)
                Spacer()
                Text("\(vm.activeCourses.count) enrolled").font(.caption).foregroundColor(.secondary)
            }
            if vm.activeCourses.isEmpty {
                emptyState("No active courses", "Enroll in courses from the Explore tab", "book.closed")
            }
            ForEach(vm.activeCourses.prefix(3)) { course in
                CourseCardView(course: course)
            }
            if vm.activeCourses.count > 3 {
                NavigationLink(destination: AllCoursesView(vm: vm)) {
                    Text("See all \(vm.activeCourses.count) courses →")
                        .font(.subheadline).foregroundColor(.indigo)
                }
            }
        }
    }
    private var dailyChallengesSection: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text("Daily Challenges").font(.headline)
                Spacer()
                Text("+\(vm.todayChallenges.reduce(0) { $0 + $1.xpReward }) XP").font(.caption).foregroundColor(.orange)
            }
            if vm.todayChallenges.isEmpty {
                emptyState("All done!", "Come back tomorrow for new challenges", "checkmark.circle.fill")
            }
            ForEach(vm.todayChallenges) { challenge in
                ChallengeCardView(challenge: challenge, onComplete: { vm.completeChallenge(challenge) })
            }
        }
    }
    private func emptyState(_ title: String, _ subtitle: String, _ symbol: String) -> some View {
        VStack(spacing: 8) {
            Image(systemName: symbol).font(.largeTitle).foregroundColor(.secondary.opacity(0.5))
            Text(title).font(.subheadline).fontWeight(.medium).foregroundColor(.secondary)
            Text(subtitle).font(.caption).foregroundColor(.secondary.opacity(0.7))
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
}
struct CourseCardView: View {
    let course: Course
    var body: some View {
        NavigationLink(destination: CourseDetailView(course: course)) {
            HStack(spacing: 14) {
                ZStack {
                    RoundedRectangle(cornerRadius: 12)
                        .fill(LinearGradient(colors: [.indigo, .purple], startPoint: .topLeading, endPoint: .bottomTrailing))
                        .frame(width: 52, height: 52)
                    Image(systemName: course.thumbnailSymbol)
                        .foregroundColor(.white)
                        .font(.title3)
                }
                VStack(alignment: .leading, spacing: 4) {
                    Text(course.title).font(.subheadline).fontWeight(.semibold)
                    Text("\(course.completedLessons)/\(course.totalLessons) lessons")
                        .font(.caption).foregroundColor(.secondary)
                    ProgressView(value: course.progress)
                        .tint(.indigo)
                }
                Spacer()
                Text("\(Int(course.progress * 100))%")
                    .font(.caption).fontWeight(.bold).foregroundColor(.indigo)
            }
            .padding()
            .background(Color(.systemBackground))
            .clipShape(RoundedRectangle(cornerRadius: 14))
            .shadow(color: .black.opacity(0.04), radius: 3, x: 0, y: 1)
        }
        .buttonStyle(.plain)
    }
}
struct ChallengeCardView: View {
    let challenge: Challenge
    let onComplete: () -> Void
    @State private var isCompleting = false
    var body: some View {
        HStack(spacing: 14) {
            ZStack {
                RoundedRectangle(cornerRadius: 10)
                    .fill(Color.orange.opacity(0.12))
                    .frame(width: 42, height: 42)
                Image(systemName: challenge.type == "quiz" ? "questionmark.bubble.fill" : challenge.type == "coding" ? "chevron.left.forwardslash.chevron.right" : challenge.type == "video" ? "play.rectangle.fill" : "person.2.fill")
                    .foregroundColor(.orange)
            }
            VStack(alignment: .leading, spacing: 2) {
                Text(challenge.title).font(.subheadline).fontWeight(.medium)
                Text(challenge.description_).font(.caption).foregroundColor(.secondary).lineLimit(1)
            }
            Spacer()
            VStack(spacing: 2) {
                Text("+\(challenge.xpReward)").font(.caption).fontWeight(.bold).foregroundColor(.orange)
                Text("XP").font(.caption2).foregroundColor(.orange.opacity(0.7))
            }
            Button(action: {
                isCompleting = true
                withAnimation { onComplete() }
                isCompleting = false
            }) {
                Text(isCompleting ? "✓" : "Go")
                    .font(.caption).fontWeight(.bold)
                    .padding(.horizontal, 14).padding(.vertical, 6)
                    .background(Color.indigo)
                    .foregroundColor(.white)
                    .clipShape(Capsule())
            }
            .disabled(isCompleting)
        }
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 14))
        .shadow(color: .black.opacity(0.04), radius: 3, x: 0, y: 1)
    }
}
struct AllCoursesView: View {
    @ObservedObject var vm: DashboardViewModel
    var body: some View {
        List {
            ForEach(vm.activeCourses) { course in
                NavigationLink(destination: CourseDetailView(course: course)) {
                    HStack {
                        Image(systemName: course.thumbnailSymbol)
                            .foregroundColor(.indigo)
                            .font(.title3)
                            .frame(width: 30)
                        VStack(alignment: .leading) {
                            Text(course.title).font(.subheadline).fontWeight(.medium)
                            ProgressView(value: course.progress).tint(.indigo)
                        }
                        Text("\(Int(course.progress * 100))%")
                            .font(.caption).fontWeight(.bold).foregroundColor(.indigo)
                    }
                }
            }
        }
        .navigationTitle("All Courses")
    }
}
struct CourseDetailView: View {
    let course: Course
    @Environment(\.modelContext) private var modelContext
    @State private var currentProgress: Double
    init(course: Course) {
        self.course = course
        _currentProgress = State(initialValue: course.progress)
    }
    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                VStack(spacing: 12) {
                    ZStack {
                        RoundedRectangle(cornerRadius: 20)
                            .fill(LinearGradient(colors: [.indigo, .purple, .blue], startPoint: .topLeading, endPoint: .bottomTrailing))
                            .frame(height: 180)
                        Image(systemName: course.thumbnailSymbol)
                            .font(.system(size: 64))
                            .foregroundColor(.white.opacity(0.8))
                    }
                    VStack(spacing: 4) {
                        Text(course.title).font(.title2).fontWeight(.bold)
                        Text(course.subtitle).font(.subheadline).foregroundColor(.secondary).multilineTextAlignment(.center)
                    }
                    HStack(spacing: 16) {
                        Label(course.difficulty, systemImage: "chart.bar.fill")
                        Label(course.category, systemImage: "folder.fill")
                        Label("\(course.totalLessons) lessons", systemImage: "list.bullet")
                    }
                    .font(.caption).foregroundColor(.secondary)
                }
                VStack(alignment: .leading, spacing: 8) {
                    Text("Progress").font(.headline)
                    ProgressView(value: currentProgress)
                        .tint(.indigo)
                        .scaleEffect(x: 1, y: 1.5, anchor: .center)
                    HStack {
                        Text("\(course.completedLessons)/\(course.totalLessons) lessons completed")
                            .font(.caption).foregroundColor(.secondary)
                        Spacer()
                        Text("\(Int(currentProgress * 100))%")
                            .font(.caption).fontWeight(.bold).foregroundColor(.indigo)
                    }
                }
                .padding()
                .background(Color(.systemBackground))
                .clipShape(RoundedRectangle(cornerRadius: 14))
                .shadow(color: .black.opacity(0.04), radius: 3, x: 0, y: 1)
                Button(action: {
                    guard currentProgress < 1.0 else { return }
                    let newProgress = min(currentProgress + 0.1, 1.0)
                    currentProgress = newProgress
                    course.progress = newProgress
                    course.completedLessons = Int(newProgress * Double(course.totalLessons))
                    StydeService.shared.updateProgress(courseId: course.id, newProgress: newProgress)
                    try? modelContext.save()
                }) {
                    Label(currentProgress >= 1.0 ? "Completed ✓" : "Continue Learning", systemImage: currentProgress >= 1.0 ? "checkmark.circle.fill" : "play.fill")
                        .font(.headline)
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(currentProgress >= 1.0 ? Color.green : Color.indigo)
                        .foregroundColor(.white)
                        .clipShape(RoundedRectangle(cornerRadius: 14))
                }
                .disabled(currentProgress >= 1.0)
            }
            .padding()
        }
        .background(Color(.systemGroupedBackground))
        .navigationBarTitleDisplayMode(.inline)
    }
}
struct ExploreView: View {
    @ObservedObject var vm: ExploreViewModel
    @Environment(\.modelContext) private var modelContext
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    searchSection
                    categoriesSection
                    recommendedSection
                    allCoursesSection
                }
                .padding()
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("Explore")
            .refreshable { vm.loadData() }
        }
        .onAppear { vm.setup(with: modelContext) }
    }
    private var searchSection: some View {
        HStack {
            Image(systemName: "magnifyingglass").foregroundColor(.secondary)
            TextField("Search courses...", text: $vm.searchQuery)
                .textFieldStyle(.plain)
                .autocorrectionDisabled()
            if !vm.searchQuery.isEmpty {
                Button(action: { vm.searchQuery = "" }) {
                    Image(systemName: "xmark.circle.fill").foregroundColor(.secondary)
                }
            }
        }
        .padding(12)
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .shadow(color: .black.opacity(0.04), radius: 3, x: 0, y: 1)
    }
    private var categoriesSection: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Trending Topics").font(.headline)
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 8) {
                    ForEach(vm.trendingTopics, id: \.0) { topic, count in
                        Button(action: { vm.selectedCategory = vm.selectedCategory == topic ? nil : topic }) {
                            HStack(spacing: 4) {
                                Text(topic).font(.caption).fontWeight(.medium)
                                Text("\(count)").font(.caption2).foregroundColor(.secondary)
                            }
                            .padding(.horizontal, 12).padding(.vertical, 6)
                            .background(vm.selectedCategory == topic ? Color.indigo : Color(.systemBackground))
                            .foregroundColor(vm.selectedCategory == topic ? .white : .primary)
                            .clipShape(Capsule())
                            .shadow(color: .black.opacity(0.04), radius: 2, x: 0, y: 1)
                        }
                    }
                }
            }
        }
    }
    private var recommendedSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Label("Recommended for You", systemImage: "sparkles").font(.headline).foregroundColor(.indigo)
                Spacer()
            }
            ScrollView(.horizontal, showsIndicators: false) {
                HStack(spacing: 14) {
                    ForEach(vm.recommendedCourses.prefix(5)) { course in
                        VStack(alignment: .leading, spacing: 6) {
                            ZStack {
                                RoundedRectangle(cornerRadius: 14)
                                    .fill(LinearGradient(colors: [.indigo, .purple], startPoint: .topLeading, endPoint: .bottomTrailing))
                                    .frame(width: 160, height: 100)
                                Image(systemName: course.thumbnailSymbol)
                                    .font(.largeTitle).foregroundColor(.white.opacity(0.8))
                            }
                            Text(course.title).font(.subheadline).fontWeight(.medium).lineLimit(1)
                            Text(course.difficulty).font(.caption2).foregroundColor(.secondary)
                            Button(action: { vm.enrollCourse(course) }) {
                                Text("Enroll").font(.caption).fontWeight(.bold)
                                    .frame(maxWidth: .infinity).padding(.vertical, 4)
                                    .background(Color.indigo).foregroundColor(.white)
                                    .clipShape(Capsule())
                            }
                        }
                        .frame(width: 160)
                    }
                }
            }
        }
    }
    private var allCoursesSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Text("All Courses").font(.headline)
                Spacer()
                if !vm.searchQuery.isEmpty || vm.selectedCategory != nil {
                    Text("\(vm.filteredCourses.count) results").font(.caption).foregroundColor(.secondary)
                }
            }
            LazyVStack(spacing: 10) {
                ForEach(vm.filteredCourses) { course in
                    NavigationLink(destination: CourseDetailView(course: course)) {
                        HStack(spacing: 12) {
                            ZStack {
                                RoundedRectangle(cornerRadius: 10)
                                    .fill(LinearGradient(colors: [.indigo.opacity(0.7), .purple.opacity(0.7)], startPoint: .topLeading, endPoint: .bottomTrailing))
                                    .frame(width: 44, height: 44)
                                Image(systemName: course.thumbnailSymbol).foregroundColor(.white)
                            }
                            VStack(alignment: .leading, spacing: 2) {
                                Text(course.title).font(.subheadline).fontWeight(.medium)
                                Text(course.subtitle).font(.caption).foregroundColor(.secondary).lineLimit(1)
                            }
                            Spacer()
                            if course.isEnrolled {
                                Text("\(Int(course.progress * 100))%")
                                    .font(.caption).fontWeight(.bold).foregroundColor(.green)
                            } else {
                                Text("New").font(.caption).fontWeight(.bold).foregroundColor(.indigo)
                            }
                            Image(systemName: "chevron.right").font(.caption2).foregroundColor(.secondary)
                        }
                        .padding()
                        .background(Color(.systemBackground))
                        .clipShape(RoundedRectangle(cornerRadius: 12))
                    }
                    .buttonStyle(.plain)
                }
            }
        }
    }
}
struct ProfileView: View {
    @ObservedObject var vm: ProfileViewModel
    @Environment(\.modelContext) private var modelContext
    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    profileHeader
                    statsGrid
                    achievementsSection
                }
                .padding()
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("Profile")
            .onAppear { vm.setup(with: modelContext) }
        }
    }
    private var profileHeader: some View {
        VStack(spacing: 12) {
            Image(systemName: vm.profile?.avatarSymbol ?? "person.circle.fill")
                .font(.system(size: 72))
                .foregroundColor(.indigo)
                .overlay(alignment: .bottomTrailing) {
                    ZStack {
                        Circle().fill(Color.green).frame(width: 20, height: 20)
                        Text("✓").font(.caption2).fontWeight(.bold).foregroundColor(.white)
                    }
                    .offset(x: -2, y: -2)
                }
            Text(vm.profile?.name ?? "Learner").font(.title2).fontWeight(.bold)
            HStack(spacing: 20) {
                Label("\(vm.profile?.totalXP ?? 0) XP", systemImage: "bolt.fill").foregroundColor(.indigo)
                Label("\(vm.profile?.streakDays ?? 0)-day streak", systemImage: "flame.fill").foregroundColor(.orange)
            }
            .font(.subheadline)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 20))
        .shadow(color: .black.opacity(0.05), radius: 4, x: 0, y: 2)
    }
    private var statsGrid: some View {
        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible()), GridItem(.flexible())], spacing: 12) {
            statCard("Courses", "\(vm.completedCourses)/\(vm.totalCourses)", "book.fill", completed: vm.totalCourses > 0)
            statCard("Challenges", "\(vm.completedChallenges)/\(vm.totalChallenges)", "flag.fill", completed: vm.totalChallenges > 0)
            statCard("Achievements", "\(vm.achievements.filter(\.isUnlocked).count)/\(vm.achievements.count)", "trophy.fill", completed: true)
        }
    }
    private func statCard(_ title: String, _ value: String, _ symbol: String, completed: Bool) -> some View {
        VStack(spacing: 4) {
            Image(systemName: symbol).font(.title3).foregroundColor(completed ? .indigo : .secondary)
            Text(value).font(.title3).fontWeight(.bold)
            Text(title).font(.caption2).foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding(.vertical, 14)
        .background(Color(.systemBackground))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }
    private var achievementsSection: some View {
        VStack(alignment: .leading, spacing: 10) {
            Text("Achievements").font(.headline)
            LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 10) {
                ForEach(vm.achievements) { achievement in
                    HStack(spacing: 10) {
                        Image(systemName: achievement.symbol)
                            .font(.title3)
                            .foregroundColor(achievement.isUnlocked ? .indigo : .secondary.opacity(0.4))
                        VStack(alignment: .leading, spacing: 1) {
                            Text(achievement.title).font(.caption).fontWeight(.medium)
                            Text(achievement.subtitle).font(.caption2).foregroundColor(.secondary).lineLimit(1)
                        }
                        Spacer()
                        if achievement.isUnlocked {
                            Image(systemName: "checkmark.seal.fill").font(.caption2).foregroundColor(.green)
                        }
                    }
                    .padding(10)
                    .background(Color(.systemBackground))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                    .opacity(achievement.isUnlocked ? 1.0 : 0.55)
                }
            }
        }
    }
}
```